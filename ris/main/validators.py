from django.core.exceptions import ValidationError

def validate_class_field(value):
    if value not in ['a','p','d','r']:
        raise ValidationError(_('%s is not a valid class key' % value), code='invalid')
