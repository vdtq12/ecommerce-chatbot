def records_to_string(records):
    result_string = ""

    # Extract field names from the first record
    field_names = records.keys()

    # Generate the string representation for each record
    for record in records:
        record_string = ", ".join([f"{field}: {record[field]}" for field in field_names])
        result_string += f"{record_string}\n"

    return result_string