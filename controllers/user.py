from flask import request, session, make_response, jsonify
from flask_restful import Resource
from config import db
from models.userModel import User

class CheckSession(Resource):
    def get(self):
        if 'user_id' in session:
            user_id = session['user_id']
            if user_id:
                user = db.session.get(User, user_id)
                if user:
                    return make_response(user.to_dict(), 200)
        return make_response({"error": "Unauthorized User Must Login"}, 401)



class Users(Resource):
    def get(self):
        return ("Hello World!")
