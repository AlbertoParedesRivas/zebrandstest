from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models.product import ProductModel
from schemas.product import ProductSchema

product_schema = ProductSchema()
product_list_schema = ProductSchema(many = True)

class Product(Resource):
    @classmethod
    def get(cls, sku: str):
        product = ProductModel.find_by_sku(sku)
        #TODO: Add view count

        if not product:
            return {"message": "Product Not Found"}, 404
        return product_schema.dump(product), 200
    
    @classmethod
    def put(cls, sku: str):
        pass
    @classmethod
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