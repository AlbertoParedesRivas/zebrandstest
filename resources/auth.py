from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from bcrypt import checkpw
from schemas.admin import AdminSchema
from models.admin import AdminModel

admin_schema = AdminSchema()

class Login(Resource):
    @classmethod
    def post(cls):
        admin_data = request.get_json()
        password = admin_data["password"].encode("utf-8")
        admin = AdminModel.find_by_email(admin_data["email"])

        if admin and checkpw(password, admin.password.encode("utf-8")):
            access_token = create_access_token(identity=admin.id)
            return {"access_token": access_token}, 200
        
        return {"message": "Invalid Credentials"}, 401