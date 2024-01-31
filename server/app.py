#!/usr/bin/env python3

import os
from flask import Flask, request, make_response, jsonify, session 
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Transaction, Category, Transaction, Budget, Transaction
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api= Api(app)
CORS(app)

class SingUp(Resource):
    def post(self):
        pass

class Login(Resource):
    def post(self):
        pass

class Logout(Resource):
    def delete(self):
        pass

class CheckSession(Resource):
    def get(self):
        pass

class TransactionResource(Resource):
    def get(self):
        pass

class CategoryResource(Resource):
    def get(self):
        pass

class BudgetResource(Resource):
    def get(self):
        pass


api.add_resource(SingUp, '/singup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(TransactionResource, '/transaction')
app.add_resource(CategoryResource, '/category')
app.add_resource(BudgetResource, '/budget')

if __name__ == '__main__':
    app.run(port=5555, debug=True)  