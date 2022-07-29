from flask import request
from flask_restful import Resource
from marshmallow import EXCLUDE
from models.admin import UserModel
from schemas.admin import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many = True)

class AdminSignUp(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_email(user.email):
            return {"message": "user_email_exists"}, 400

        try:
            user.save_to_db()
            return user_schema.dump(user), 200
        except:
            user.delete_from_db()
            return {"message": "user_error_creating"}, 500

class Admin():
    @classmethod
    def get(cls, admin_id: int):
        pass
    def delete(cls, admin_id: int):
        pass

class AdminList(Resource):
    @classmethod
    def get(cls):
        return {"users": user_list_schema.dump(UserModel.find_all())}, 200
        