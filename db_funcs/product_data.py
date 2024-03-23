from ..extensions import db

def get_product_data(sql): 
    for record in db.engine.execute(sql): 
        print(record) 