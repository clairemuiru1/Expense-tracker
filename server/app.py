#!/usr/bin/env python3

import os
from flask import Flask, request, make_response, jsonify, session, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, IntegerField
from sqlalchemy.exc import IntegrityError
from models import db, Transaction, Budget, Category, User, Bill
from flask_cors import CORS
from flask_restful import reqparse
import jwt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    JWTManager,
    create_access_token,
)
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = b"BM3\x1d\x16z!\x0e:\x8b&\xe6"
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_QUERY_STRING_NAME"] = "token"
app.config["JWT_QUERY_STRING_VALUE_PREFIX"] = "Bearer"

db.init_app(app)
bcrypt = Bcrypt(app)
api = Api(app)
migrate = Migrate(app, db)
CORS(app)
jwt = JWTManager(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            return jsonify({"Alert!": "Token is missing"}), 401
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"])
        except jwt.ExpiredSignatureError:
            return jsonify({"Alert!": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"Alert!": "Invalid Token!"}), 401
        return func(*args, **kwargs)

    return decorated


class SignupForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    email = StringField("Email", [validators.Email()])
    password = PasswordField(
        "Password", [validators.DataRequired(), validators.Length(min=6)]
    )


class Signup(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON format"}, 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"error": "Missing required fields"}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(username=username, email=email, _password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()

            # Initialize user's profile with zero bills, budgets, and transactions
            new_user.bills = []
            new_user.budgets = []
            new_user.transactions = []

            db.session.commit()

            return {"message": "User created successfully"}, 200
        except IntegrityError:
            db.session.rollback()
            return {
                "error": "Username or email already exists. Please choose a different one."
            }, 400


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Missing username or password"}, 400

        # Replace this logic with your actual authentication mechanism (e.g., querying the database)
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user._password_hash, password):
            access_token = create_access_token(identity=user.id)
            return {"token": access_token}, 200
        else:
            return {"error": "Invalid username or password"}, 401


class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        return {"message": "Logout successful"}, 200


@app.route("/public")
def public():
    return "for public"


@app.route("/auth")
@token_required
def auth():
    return "JWT is verified. Welcome to your dashboard"


class CheckSession(Resource):
    def get(self):

        user_id = session["user_id"]
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200

        return {}, 401


class TransactionForm(FlaskForm):
    amount = IntegerField("amount", [validators.DataRequired()])
    description = StringField("description", [validators.DataRequired()])
    category = StringField("category", [validators.DataRequired()])


class TransactionResource(Resource):
    def get(self):
        transactions = []
        for transaction in Transaction.query.all():
            transaction_dict = {
                "id": transaction.id,
                "amount": transaction.amount,
                "date": transaction.date,
                "description": transaction.description,
                "category": {},
            }
            if transaction.category:
                transaction_dict["category"] = {
                    "id": transaction.category.id,
                    "name": transaction.category.name,
                }
            transactions.append(transaction_dict)

        response = make_response(jsonify(transactions), 200)
        return response

    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON format"}, 400

        amount = data.get("amount")
        description = data.get("description")
        category_name = data.get("category")

        if not all([amount, description, category_name]):
            return {"error": "Missing required fields"}, 400

        # Convert amount to integer
        try:
            amount = int(amount)
        except ValueError:
            return {"error": "Amount must be a valid integer"}, 400

        category = Category.query.filter_by(name=category_name).first()

        if not category:
            return {"error": f"Category '{category_name}' does not exist"}, 404

        # Deduct transaction amount from category budget
        budget = Budget.query.filter_by(Category_id=category.id).first()

        if not budget:
            return {"error": f"No budget found for category '{category_name}'"}, 404

        budget.amount -= amount

        new_transaction = Transaction(
            amount=amount,
            description=description,
            category=category,
            date=datetime.utcnow(),
        )

        try:
            db.session.add(new_transaction)
            db.session.commit()

            # Update category budget in the database
            db.session.commit()

            return {"message": "Transaction created successfully"}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"error": str(e)}, 500


class CategoryResource(Resource):
    def get(self):
        categories = []
        for category in Category.query.all():
            category_dict = {
                "id": category.id,
                "name": category.name,
            }
            categories.append(category_dict)

        response = make_response(jsonify(categories))
        return response


class BudgetForm(FlaskForm):
    amount = StringField("amount", [validators.DataRequired()])
    category = StringField("category", [validators.DataRequired()])


class BudgetResource(Resource):
    def get(self):
        budgets = []
        for budget in Budget.query.all():
            budget_dict = {
                "id": budget.id,
                "amount": budget.amount,
                "category": {"name": budget.category.name},
            }
            budgets.append(budget_dict)

        response = make_response(jsonify(budgets), 200)
        return response

    @jwt_required()
    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON format"}, 400

        amount = data.get("amount")
        category_name = data.get("category")

        if not amount or not category_name:
            return {"error": "Missing required fields"}, 400

        # Check if the category exists
        category = Category.query.filter_by(name=category_name).first()

        if not category:
            return {"error": f"Category '{category_name}' does not exist"}, 404

        # Get the authenticated user ID from the JWT token
        user_id = get_jwt_identity()

        # Query the User model to get the user object
        user = User.query.get(user_id)
        if not user:
            return {"error": "Invalid user"}, 400

        # Create a new budget with the associated category and user
        new_budget = Budget(amount=amount, category=category, user=user)

        try:
            db.session.add(new_budget)
            db.session.commit()
            return {"message": "Budget created successfully"}, 200
        except IntegrityError:
            db.session.rollback()
            return {"error": "Invalid JSON format"}, 500


class BudgetByID(Resource):
    def get(self, id):
        budget = Budget.query.get(id)

        if not budget:
            return {"error": f"Budget with id {id} not found"}, 404

        budget_dict = {
            "id": budget.id,
            "amount": budget.amount,
            "user_id": budget.User_id,
            "category_id": budget.Category_id,
        }

        response = make_response(jsonify(budget_dict), 200)
        return response

    def patch(self, id):
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON format"}, 400

        new_amount = data.get("amount")

        if not new_amount:
            return {"error": "Missing required fields"}, 400

        budget = Budget.query.get(id)

        if not budget:
            return {"error": f"Budget with id {id} not found"}, 404

        budget.amount = new_amount

        try:
            db.session.commit()
            return {"message": "Budget updated successfully"}, 200
        except IntegrityError:
            db.session.rollback()
            return {"error": "Invalid JSON format"}, 500

    def delete(self, id):
        budget = Budget.query.get(id)

        if not budget:
            return {"error": f"Budget with id {id} not found"}, 404

        try:
            db.session.delete(budget)
            db.session.commit()
            return {"message": "Budget deleted successfully"}, 200
        except IntegrityError:
            db.session.rollback()
            return {"error": "Error deleting the budget"}, 500


class BillResource(Resource):
    def get(self):
        bills = []
        for bill in Bill.query.all():
            bill_dict = {
                "id": bill.id,
                "title": bill.bill_title,
                "amount": bill.amount,
                "date": bill.date.strftime("%Y-%m-%d"),  # Assuming you want date in a specific format
            }
            bills.append(bill_dict)

        response = make_response(jsonify(bills), 200)
        return response

    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON format"}, 400

        bill_title = data.get("bill_title")
        amount = data.get("amount")
        date_str = data.get("date")

        if not amount or not date_str or not bill_title:
            return {"error": "Missing required fields"}, 400

        try:
            # Convert date string to Python date object
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return {
                "error": "Invalid date format. Please provide date in YYYY-MM-DD format."
            }, 400

        new_bill = Bill(amount=amount, date=date, bill_title=bill_title)

        try:
            db.session.add(new_bill)
            db.session.commit()
            return {"message": "Bill created successfully"}, 200
        except IntegrityError:
            db.session.rollback()
            return {"error": "Failed to create bill"}, 500


class BillByID(Resource):
    def get(self, bill_id):
        bill = Bill.query.get(bill_id)

        if not bill:
            return {"error": f"Bill with id {bill_id} not found"}, 404

        bill_dict = {
            "id": bill.id,
            "title": bill.title,
            "amount": bill.amount,
            "date": bill.date.strftime("%Y-%m-%d"),
        }

        response = make_response(jsonify(bill_dict), 200)
        return response

    def patch(self, bill_id):
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON format"}, 400

        new_title = data.get("title")

        if not new_title:
            return {"error": "No title provided for update"}, 400

        bill = Bill.query.get(bill_id)

        if not bill:
            return {"error": f"Bill with id {bill_id} not found"}, 404

        bill.title = new_title

        try:
            db.session.commit()
            return {"message": "Bill title updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        
    def delete(self, bill_id):
        bill = Bill.query.get(bill_id)

        if not bill:
            return {"error": f"Bill with id {bill_id} not found"}, 404

        try:
            db.session.delete(bill)
            db.session.commit()
            return {"message": "Bill deleted successfully"}, 200
        except IntegrityError:
            db.session.rollback()
            return {"error": "Failed to delete bill"}, 500


api.add_resource(BillResource, "/bills")
api.add_resource(BillByID, "/bills/<int:bill_id>")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(TransactionResource, "/transactions")
api.add_resource(CategoryResource, "/categories")
api.add_resource(BudgetResource, "/budgets")
api.add_resource(BudgetByID, "/budgets/<int:id>")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
