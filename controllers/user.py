from flask import request, session, make_response, jsonify
from flask_restful import Resource

class UserHome(Resource):
    def get(self):
        return ("Hello World!")
