from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)

    def __repl__(self):
        return f'user{self.username} , id{self.id}'
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        # utf-8 encoding and decoding is required in python 3
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    transactions = db.relationship('Transaction', backref='user')
    budgets = db.relationship('Budget', backref='user')

class Transaction(db.Model ,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.String , nullable=True)
    User_id = db.Column( db.Integer, db.ForeignKey('user.id'))
    Category_id = db.Column(db.Integer,db.ForeignKey('category.id'))

class Category(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    transactions = db.relationship('Transaction', backref='category')
    budgets = db.relationship('Budget', backref='category')

class Budget(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    User_id = db.Column( db.Integer, db.ForeignKey('user.id'))
    Category_id = db.Column(db.Integer,db.ForeignKey('category.id'))