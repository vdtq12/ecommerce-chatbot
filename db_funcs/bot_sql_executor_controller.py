from ..extensions import db

def records_to_string(records):
    result_string = ""

    # Extract field names from the first record
    field_names = records.keys()

    # Generate the string representation for each record
    for record in records:
        record_string = ", ".join([f"{field}: {record[field]}" for field in field_names])
        result_string += f"{record_string}\n"

    return result_string

def double_percent(string):
    return string.replace('%', '%%')

def get_product_data(sql): 
    modified_sql = double_percent(sql)
    records = db.engine.execute(modified_sql)
    
    if int(records.rowcount) > 0:
        records = records_to_string(records)
        print(f"records found: {records} - end.")
        return records
    else:
        return "can not find the result"
    
