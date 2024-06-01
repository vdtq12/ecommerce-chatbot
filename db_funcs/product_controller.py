from sqlalchemy.orm import aliased

from ..extensions import db
from ..models.product import Product
from ..models.productline import Product_line
from .bot_sql_executor_controller import records_to_string

def get_product_local_specs(catergory_name):
    # Product_line1 = aliased(Product_line)
    # Product = aliased(Product)
    products = Product.query.with_entities(Product.id, Product.local_specs).select_from(Product).join(Product_line, Product.product_line == Product_line.id).filter(Product_line.category.ilike(f'%%{catergory_name}%%')).all()

    if len(products) > 0:
        # records = records_to_string(products)
        print(f"records found: {len(products)} - end.")
        print(f"records found: {products} - end.")
        return products
    else:
        return "can not find the result"
    
def get_product_by_id(product_id):
    product = Product.query.with_entities(Product.name, Product.local_specs).filter_by(id=product_id).first()
    if product:
        return product
    else:
        return None