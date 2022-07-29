from flask import Flask, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from common.db import db
from common.ma import ma
from resources.admin import AdminSignUp, Admin

app = Flask(__name__)
app.config.from_object("default_config")
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

api.add_resource(AdminSignUp, "/admins")
api.add_resource(Admin, "/admins/<string:admin_id>")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)