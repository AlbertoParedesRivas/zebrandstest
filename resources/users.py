from flask_restful import Resource

class AdminSignUp(Resource):
    def post(self):
        return {"message": "adminSignUp"}