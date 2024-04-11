from ..extensions import db
from .records_to_string import records_to_string

def double_percent(string):
    return string.replace('%', '%%')

def get_product_data(sql): 
    modified_sql = double_percent(sql)
    records = db.engine.execute(modified_sql)

    print(f"records row count: {records.rowcount}")

    if int(records.rowcount) > 0:
        records = records_to_string(records)
        print(f"records found: {records} - end.")
        return records
    else:
        return "can not find the result"