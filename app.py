from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from common.db import db
from common.ma import ma
from resources.admin import AdminSignUp, Admin, firstAdmin
from resources.auth import Login
from resources.product import Product, RegisterProduct

app = Flask(__name__)
app.config.from_object("default_config")
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()
    firstAdmin()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

jwt = JWTManager(app)

api.add_resource(Login, "/login")
api.add_resource(AdminSignUp, "/admins")
api.add_resource(Admin, "/admins/<string:admin_id>")
api.add_resource(Product, "/products/<string:sku>")
api.add_resource(RegisterProduct, "/products")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, host="0.0.0.0")