from flask import request, session, make_response, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from models.userModel import User
from config import db

class CheckSession(Resource):
    def get(self):
        if 'user_id' in session:
            user_id = session['user_id']
            if user_id:
                user = db.session.get(User, user_id)
                if user:
                    return make_response(user.to_dict(), 200)
        return make_response({"error": "Unauthorized User Must Login"}, 401)

class SignUp(Resource):
    def post(self):
        params = request.get_json()
        username = params.get('username')
        email = params.get('email')
        password = params.get('password')
        
        user = User(
            username=username,
            email=email
        )
        user.password_hash = password
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return make_response(user.to_dict(), 201)
        except IntegrityError as e:
            print(e)
            return make_response({"error": "422 unprocessable Entity", "details": str(e)}, 422)
        
class Login(Resource):
    def post(self):
        params = request.json
        username= params.get('username')
        user = User.query.filter(User.username == params.get('username')).first()
        if not user:
            return make_response({"Error": "User not found"})
        if user.authenticate(params.get('password')):
            session['user_id'] = str(user.id)
            return make_response(user.to_dict())
        else:
            return make_response({"Error": "Invalid password"}, 401)

class Users(Resource):
    def get(self):
        return ("Hello World!")
