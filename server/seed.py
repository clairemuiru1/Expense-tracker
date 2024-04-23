from app import db, app
from models import Category

with app.app_context():
    db.drop_all()  # Drop all tables from the database
    db.create_all()

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

    with app.app_context():
        for category_data in categories_data:
            category = Category(**category_data)
            db.session.add(category)
        db.session.commit()
