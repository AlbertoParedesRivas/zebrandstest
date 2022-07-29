from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models.admin import AdminModel
from schemas.admin import AdminSchema
from common.util import is_valid_uuid

admin_schema = AdminSchema()
admin_list_schema = AdminSchema(many = True)

class AdminSignUp(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        admin = admin_schema.load(request.get_json())

        if AdminModel.find_by_email(admin.email):
            return {"message": "Email already registered"}, 400

        try:
            admin.save_to_db()
            return admin_schema.dump(admin), 200
        except:
            return {"message": "Error creating admin"}, 500
    
    @classmethod
    @jwt_required()
    def get(cls):
        return {"admins": admin_list_schema.dump(AdminModel.find_all())}, 200


class Admin(Resource):
    @classmethod
    @jwt_required()
    def get(cls, admin_id: str):
        if is_valid_uuid(admin_id):
            admin = AdminModel.find_by_id(admin_id)
        else:
            admin = None

        if not admin:
            return {"message": "admin_not_found"}, 404
        return admin_schema.dump(admin), 200

    @classmethod
    @jwt_required()
    def delete(cls, admin_id: str):
        if is_valid_uuid(admin_id):
            admin = AdminModel.find_by_id(admin_id)
        else:
            admin = None

        if not admin:
            return {"message": "admin_not_found"}, 404
        admin.delete_from_db()
        return {"message": "admin_deleted"}, 200
    
    @classmethod
    @jwt_required()
    def put(cls, admin_id: str):
        admin_json = admin_schema.load(request.get_json())

        if AdminModel.find_by_email(admin_json.email):
            return {"message": "admin_email_exists"}, 400
        
        if is_valid_uuid(admin_id):
            admin = AdminModel.find_by_id(admin_id)
        else:
            admin = None

        if admin:
            admin.name = admin_json.name
            admin.lastname = admin_json.lastname
            admin.email = admin_json.email
            admin.password = admin_json.password
        else:
            admin = admin_json
        
        admin.save_to_db()
        return admin_schema.dump(admin), 200