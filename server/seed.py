from app import db, bcrypt, app
from models import User, Transaction, Category, Budget

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

    with app.app_context():
        seed_categories(categories_data)
        seed_transactions(transactions_data)
        seed_budgets(budgets_data)
