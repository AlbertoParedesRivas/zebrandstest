from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restful import Resource
from models.product import ProductModel
from schemas.product import ProductSchema
from models.product_view import ProductViewModel

product_schema = ProductSchema()
product_list_schema = ProductSchema(many = True)

class Product(Resource):
    @classmethod
    def get(cls, sku: str):
        product = ProductModel.find_by_sku(sku)

        if not product:
            return {"message": "Product Not Found"}, 404
        
        if not verify_jwt_in_request(optional=True):
            product_views = ProductViewModel(productId=product.id)
            product_views.save_to_db()
            
        print(product.views)

        return product_schema.dump(product), 200
    
    @classmethod
    @jwt_required()
    def put(cls, sku: str):
        product_json = product_schema.load(request.get_json())
        product = ProductModel.find_by_sku(sku)

        if not product:
            return {"message": "Product Not Found"}, 404
        if ProductModel.find_by_sku(product_json.sku):
            return {"message": "SKU already registered"}, 400
        
        product.name = product_json.name
        product.price = product_json.price
        product.stock = product_json.stock
        product.brand = product_json.brand
        product.sku = product_json.sku
        
        product.save_to_db()

        # TODO Add notification feature

        return product_schema.dump(product), 200

    @classmethod
    @jwt_required()
    def delete(cls, sku: str):
        product = ProductModel.find_by_sku(sku)
        #TODO: Add notification feature

        if not product:
            return {"message": "Product Not Found"}, 404

        product.delete_from_db()
        return {"message": "Product Deleted"}, 200
        

class RegisterProduct(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        product = product_schema.load(request.get_json())

        if ProductModel.find_by_sku(product.sku):
            return {"message": "SKU already registered"}, 400
        # TODO: Add notification feature
        try:
            product.save_to_db()
            return product_schema.dump(product), 200
        except:
            return {"message": "Error creating product"}, 500
        

    @classmethod
    def get(cls):
        return {"products": product_list_schema.dump(ProductModel.find_all())}, 200