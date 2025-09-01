# app/database.py

from sqlmodel import create_engine, Session, SQLModel
from .models import Milk

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        milk_stock = session.get(Milk, 1)
        if not milk_stock:
            initial_milk = Milk(stock_ml=10000.0)
            session.add(initial_milk)
            session.commit()
            print("Initial milk stock created.")

def get_session():
    with Session(engine) as session:
        yield session