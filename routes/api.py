# from flask import Blueprint
# from ..models.productline import ProductLine
# from ..extensions import db

# api = Blueprint('api', __name__)

# @api.route('/get')
# def chat():
#     # query = request.form["msg"]
#     # _response = get_Chat_response(query)

#     products=ProductLine.query.limit(5).all()
    
#     for product in products:
#         print(product.id, product.category, product.supplier, product.name, product.description)
#     return 'hi'
