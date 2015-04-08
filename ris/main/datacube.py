from main.models import RadiologyRecord
from django.db import models, connection

def olap_aggregator(patient_id=None, test_type=None, test_date=None, start_date=None, end_date=None):
    assert test_date in [ False, 'year', 'week', 'month']

    dbquery = "SELECT {0}, {1}, {2}, count(pacs_images.image_id) FROM radiology_record, pacs_images {4} GROUP BY {3} {5};"

    zero = "patient_id" if patient_id else "null"
    one = "test_type" if test_type else "null"
    two = "date_trunc('%s', test_date)"%(test_date) if test_date else "null"

    # GROUP BY clause
    three = ""
    if patient_id: three += "patient_id, "
    if test_type:    three += "test_type, "
    if test_date:     three += "3, "
    if len(three) > 0: three = three[:-2]

    # WHERE clause
    four = "WHERE pacs_images.record_id = radiology_record.record_id"
    if start_date or end_date:
        four += " AND "
    if start_date:
        four += "test_date >= '%s' " % start_date
    elif end_date:
        four += "test_date < ('%s'::date + '1 day'::interval) " % end_date
    if end_date and start_date:
        four += "AND test_date < ('%s'::date + '1 day'::interval) " % end_date

    # ORDER BY clause
    five = "ORDER BY date_trunc('%s', test_date)"%(test_date) if test_date else ''

    dbquery = dbquery.format(zero, one, two, three, four, five)
    if not any([patient_id, test_type, test_date]):
        dbquery = dbquery[:-11]

    cursor = connection.cursor()
    cursor.execute(dbquery)
    result = cursor.fetchall()

    data = list()

    for db_row in result:
        row = dict()
        if patient_id:
            if db_row[0] is None:
                row["patient"] = "&lt;No patient&gt;"
            else:
                row["patient"] = db_row[0]
        if test_type:
            if db_row[1] is None:
                row["test_type"] = "&lt;No test_type&gt;"
            else:
                row["test_type"] = db_row[1]
        if test_date:
            # test_date_col = {"year":"Year", "Month
            if db_row[2] is None:
                row["test_date"] = "&lt;No Date&gt;"
            elif test_date == 'year':
                row["test_date"] = "%d" % (db_row[2].year)
            elif test_date == 'month':
                row["test_date"] = "%d-%02d" % (db_row[2].year, db_row[2].month)
            elif test_date == 'week':
                row["test_date"] = "%d-%02d-%02d" % (db_row[2].year, db_row[2].month, db_row[2].day)

        row["image_count"] = db_row[3]
        data.append(row)
