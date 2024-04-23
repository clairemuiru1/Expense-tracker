from app import db, bcrypt, app
from models import User, Transaction, Category, Budget, Bill
from datetime import datetime  # Add this import

with app.app_context():
    db.drop_all()
    db.create_all()
    
def seed_users(users_data):
    print(":bust_in_silhouette: Seeding users...")
    for user_data in users_data:
        user = User(**user_data)
        # Hashing the password before storing it in the database
        user.password_hash = bcrypt.generate_password_hash(user_data["password_hash"]).decode('utf-8')
        db.session.add(user)
    db.session.commit()
    print("User seeding completed.")

def seed_categories(categories_data):
    print(":label: Seeding categories...")
    for category_data in categories_data:
        category = Category(**category_data)
        db.session.add(category)
    db.session.commit()
    print("Category seeding completed.")

def seed_transactions(transactions_data):
    print(":money_with_wings: Seeding transactions...")
    for transaction_data in transactions_data:
        # Convert the date string to a datetime object
        transaction_data['date'] = datetime.strptime(transaction_data['date'], '%Y-%m-%dT%H:%M:%S')
        
        transaction = Transaction(**transaction_data)
        db.session.add(transaction)
    db.session.commit()
    print("Transaction seeding completed.")

def seed_budgets(budgets_data):
    print(":chart_with_upwards_trend: Seeding budgets...")
    for budget_data in budgets_data:
        budget = Budget(**budget_data)
        db.session.add(budget)
    db.session.commit()
    print("Budget seeding completed.")

from datetime import datetime

def seed_bills(bills_data):
    print(":moneybag: Seeding bills...")
    for bill_data in bills_data:
        # Convert the date string to a Python date object
        bill_data['date'] = datetime.strptime(bill_data['date'], '%Y-%m-%d')
        
        bill = Bill(**bill_data)
        db.session.add(bill)
    db.session.commit()
    print("Bill seeding completed.")
    
if __name__ == '__main__':
    categories_data = [
        {"name": "Groceries"},
        {"name": "Entertainment"},
        {"name": "Utilities"},
        {"name": "Transportation"},
        {"name": "Healthcare"},
        {"name": "Education"},
        {"name": "Other"},
    ]

    transactions_data = [
        {"amount": 50, "date": "2024-01-31T12:00:00", "description": "Grocery shopping", "User_id": 1, "Category_id": 1},
        {"amount": 20, "date": "2024-01-30T14:30:00", "description": "Movie night", "User_id": 2, "Category_id": 2},
        {"amount": 100, "date": "2024-01-29T10:45:00", "description": "Electricity bill", "User_id": 3, "Category_id": 3},
        # Add more transactions as needed
    ]

    budgets_data = [
        {"amount": 200, "User_id": 1, "Category_id": 1},
        {"amount": 50, "User_id": 2, "Category_id": 2},
        {"amount": 150, "User_id": 3, "Category_id": 3},
        # Add more budgets as needed
    ]

    bills_data = [
        {"bill_title": "Rent", "amount": 1000, "date": "2024-04-01", "User_id": 1},
        {"bill_title": "Internet", "amount": 50, "date": "2024-04-10", "User_id": 2},
        {"bill_title": "Phone", "amount": 30, "date": "2024-04-15", "User_id": 3},
        # Add more bills as needed
    ]

    users_data = [
        {"username": "user1", "email": "user1@example.com", "password_hash": "password1"},
        {"username": "user2", "email": "user2@example.com", "password_hash": "password2"},
        {"username": "user3", "email": "user3@example.com", "password_hash": "password3"},
        # Add more users as needed
    ]

    with app.app_context():
        seed_categories(categories_data)
        seed_transactions(transactions_data)
        seed_budgets(budgets_data)
        seed_bills(bills_data)
        seed_users(users_data)
