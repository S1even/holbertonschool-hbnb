from app import create_app, db
from app.seed import seed_database
import os

app = create_app()

if __name__ == '__main__':
    """Delete existing database file if it exists"""
    db_file = 'development.db'
    if os.path.exists(db_file):
        os.remove(db_file)
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database()
    app.run(debug=True)