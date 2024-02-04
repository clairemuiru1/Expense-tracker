#!/usr/bin/env python3

import os
from flask import Flask, request, make_response, jsonify, session, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from sqlalchemy.exc import IntegrityError
from models import db, Transaction, Budget, Category, User
from flask_cors import CORS
from flask_restful import reqparse
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'BM3\x1d\x16z!\x0e:\x8b&\xe6'

db.init_app(app)
bcrypt = Bcrypt(app)
api = Api(app)
CORS(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing'}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert!': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'Alert!': 'Invalid Token!'}), 401
        return func(*args, **kwargs)

    return decorated


class SignupForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6)])


class Signup(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {'error': 'Invalid JSON format'}, 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {'error': 'Missing required fields'}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, _password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username or email already exists. Please choose a different one.'}, 400


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'error': 'Missing username or password'}, 400

        # Replace this logic with your actual authentication mechanism (e.g., querying the database)
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user._password_hash, password):
            token = jwt.encode({
                'user': username,
                'expiration': str(datetime.utcnow() + timedelta(seconds=120))
            },
                app.config['SECRET_KEY'])

            return {'token': token}

        else:
            return {'error': 'Invalid username or password'}, 401


class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {'message': 'Logout successful'}, 204


@app.route('/public')
def public():
    return 'for public'


@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard'


class CheckSession(Resource):
    def get(self):
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return "Logged in currently"


class TransactionResource(Resource):
    def get(self):
        transactions = []
        for transaction in Transaction.query.all():
            transaction_dict = {
                "id": transaction.id,
                "amount": transaction.amount,
                "date": transaction.date,
                "description": transaction.description,
                "category": {
                    "id": transaction.category.id,
                    "name": transaction.category.name
                }
            }
            transactions.append(transaction_dict)

        response = make_response(
            jsonify(transactions),
            200
        )
        return response

    def post(self):

        new_transaction = Transaction(
            amount = request.form['amount'],
            description = request.form['description'],
            Category_id = request.form['category_id'],
        )
        db.session.add(new_transaction)
        db.session.commit()

        response_dict = new_transaction.to_dict()

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

class CategoryResource(Resource):
    def get(self):
        categories = []
        for category in Category.query.all():
            category_dict = {
                "id": category.id,
                "name": category.name,
            }
            category.append(category_dict)

        response = make_response(
            jsonify(categories)
        )
        return response


class BudgetResource(Resource): 
    def get(self):
        budgets = []
        for budget in Budget.query.all():
            budget_dict = {
                "id": budget.id,
                "amount": budget.amount,
                "category":{
                    budget.category.name
                }
            }
            budget.append(budget_dict)

        response = make_response(
            jsonify(budgets),
            200
        )
        return response

# class BudgetByID(Resource):
#     def patch(self,id):

        
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(TransactionResource, '/transactions')
api.add_resource(CategoryResource, '/categories')
api.add_resource(BudgetResource, '/budgets')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
