#!/usr/bin/env python3
from flask import request, session, make_response, jsonify
from flask_restful import Resource
from config import start_app
from flask_restful import Api
from controllers.home import Home
from controllers.user import Users, CheckSession, SignUp, Login, Logout, GetHabitsByUserAndDateRange
from controllers.habits import HabitController, HabitById
from flask_bcrypt import Bcrypt

app = start_app()
api = Api(app)
bcrypt = Bcrypt(app)
api.add_resource(Home, '/')
api.add_resource(Users, '/users')
api.add_resource(CheckSession, '/check_session')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(HabitController, '/habit')
api.add_resource(HabitById, '/habits/<id>')
api.add_resource(GetHabitsByUserAndDateRange, '/habits_by_user/<id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)