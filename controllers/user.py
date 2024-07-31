from flask import request, session, make_response, jsonify
from flask_restful import Resource

class Home(Resource):
    def get(self):
        return ("Hello World!")
