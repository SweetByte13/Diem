#!/usr/bin/env python3
from flask import request, session, make_response, jsonify
from flask_restful import Resource
from config import app, db, api
from controllers.user import Home 

api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(port=5555, debug=True)