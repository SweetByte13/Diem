#!/usr/bin/env python3
from flask import request, session, make_response, jsonify
from flask_restful import Resource
from config import app, db, api
from controllers.home import Home
from controllers.user import Users, CheckSession

api.add_resource(Home, '/')
api.add_resource(Users, '/users')
api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)