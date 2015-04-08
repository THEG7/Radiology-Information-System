from main.models import RadiologyRecord, Person
from django.db.models import Q
import re

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default


def full_name_frequency(record, keywords):
    frequency = 0
    for word in keywords:
        frequency += (record.patient.first_name.count(word) + record.patient.last_name.count(word))/2
    return frequency

def diagnosis_frequency(record, keywords):
    frequency = 0
    for word in keywords:
        frequency += record.diagnosis.count(word)
    return frequency

def description_frequency(record, keywords):
    frequency = 0
    for word in keywords:
        frequency += record.description.count(word)
    return frequency

 # Rank(record_id) = 6*frequency(patient_name) + 3*frequency(diagnosis) + frequency(description)
def rank_function(record, query_string):
    key_words = normalize_query(query_string)
    name_weight = (6*full_name_frequency(record, key_words))
    diagnosis_weight = (3*diagnosis_frequency(record, key_words))
    description_weight = description_frequency(record, key_words)
    return (name_weight + diagnosis_weight + description_weight)


# adapted from http://stackoverflow.com/questions/26634874/how-can-i-make-django-search-in-multiple-fields-using-querysets-and-mysql-full
def normalize_query(query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):

    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace('',(t[0] or t[1]).strip()) for t in findterms(query_string)]

def build_search_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects.
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query
