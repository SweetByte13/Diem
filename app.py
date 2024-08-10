#!/usr/bin/env python3
from flask import request, session, make_response, jsonify
from flask_restful import Resource
from config import start_app
from flask_restful import Api
from controllers.home import Home
from controllers.user import Users, CheckSession, SignUp
from flask_bcrypt import Bcrypt

app = start_app()
api = Api(app)
bcrypt = Bcrypt(app)
api.add_resource(Home, '/')
api.add_resource(Users, '/users')
api.add_resource(CheckSession, '/check_session')
api.add_resource(SignUp, '/signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)