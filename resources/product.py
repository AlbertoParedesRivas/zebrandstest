from flask import request
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from flask_restful import Resource
from common.mailgun import MailgunException
from models.product import ProductModel
from schemas.product import ProductSchema
from models.product_view import ProductViewModel
from common.notification import sendNotification

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
        productFromJsonSku = ProductModel.find_by_sku(product_json.sku)
        if productFromJsonSku and product.id != productFromJsonSku.id:
            return {"message": "SKU already registered"}, 400
        
        updatedFields = []
        
        if product.name != product_json.name:
            product.name = product_json.name
            updatedFields.append("name")
            
        if product.price != product_json.price:
            product.price = product_json.price
            updatedFields.append("price")
        
        if product.stock != product_json.stock:
            product.stock = product_json.stock
            updatedFields.append("stock")

        if product.brand != product_json.brand:
            product.brand = product_json.brand
            updatedFields.append("brand")

        if product.sku != product_json.sku:
            product.sku = product_json.sku
            updatedFields.append("sku")
        
        product.save_to_db()
        claims = get_jwt()
        
        try: 
            sendNotification("UPDATE", {"author": claims["name"], "sku": product.sku, "name": product.name, "updatedFields": updatedFields})
        except MailgunException as e:
            return {"message": str(e)}, 500


        return product_schema.dump(product), 200

    @classmethod
    @jwt_required()
    def delete(cls, sku: str):
        product = ProductModel.find_by_sku(sku)

        if not product:
            return {"message": "Product Not Found"}, 404

        product.delete_from_db()

        claims = get_jwt()
        try:
            sendNotification("DELETE", {"author": claims["name"], "sku": product.sku, "name": product.name})
        except MailgunException as e:
            return {"message": str(e)}, 500

        return {"message": "Product Deleted"}, 200
        

class RegisterProduct(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        product = product_schema.load(request.get_json())

        if ProductModel.find_by_sku(product.sku):
            return {"message": "SKU already registered"}, 400
        try:
            product.save_to_db()

            claims = get_jwt()
            try:
                sendNotification("REGISTER", {"author": claims["name"], "sku": product.sku, "name": product.name})
            except MailgunException as e:
                return {"message": str(e)}, 500

            return product_schema.dump(product), 200
        except:
            return {"message": "Error creating product"}, 500
        

    @classmethod
    def get(cls):
        return {"products": product_list_schema.dump(ProductModel.find_all())}, 200