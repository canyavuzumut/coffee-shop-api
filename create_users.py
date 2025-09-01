import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, create_db_and_tables
from app.models import User
from app.auth import get_password_hash
from sqlmodel import Session, select
from datetime import timedelta

def create_initial_users():
    
    print("Creating initial users...")
    
    
    create_db_and_tables()

    with Session(engine) as session:
        manager = session.exec(select(User).where(User.username == "yonetici")).first()
        if not manager:
            hashed_password = get_password_hash("sifre123")
            manager = User(username="yonetici", password=hashed_password, role="manager")
            session.add(manager)
            print("Manager user created.")

        employee = session.exec(select(User).where(User.username == "calisan")).first()
        if not employee:
            hashed_password = get_password_hash("sifre123")
            employee = User(username="calisan", password=hashed_password, role="employee")
            session.add(employee)
            print("Employee user created.")
        
        session.commit()
        print("Users committed to the database.")

if __name__ == "__main__":
    create_initial_users()