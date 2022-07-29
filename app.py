import imp
from flask import Flask
from flask_restful import Api

from resources.users import AdminSignUp


app = Flask(__name__)
api = Api(app)

api.add_resource(AdminSignUp, "/admin/signup")

if __name__ == '__main__':
    app.run(debug=True)