from typing import Optional, List
from sqlmodel import Field, SQLModel
from datetime import date

class CoffeeBase(SQLModel):
    name: str = Field(index=True)
    price: float
    stock_grams: float

class Coffee(CoffeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class RecipeBase(SQLModel):
    coffee_id: int = Field(foreign_key="coffee.id")
    milk_ml: float
    coffee_grams: float

class Recipe(RecipeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class SaleBase(SQLModel):
    coffee_id: int = Field(foreign_key="coffee.id")
    quantity: int
    total_price: float
    sale_date: date

class Sale(SaleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class Milk(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    stock_ml: float = 0.0

# SaleRequest sınıfını, onu kullanan fonksiyondan önce tanımla
class SaleRequest(SQLModel):
    coffee_id: int
    quantity: int

class SalesReport(SQLModel):
    total_sales: float
    total_quantity: int

class StockUpdate(SQLModel):
    new_stock: float

class TopSellingItem(SQLModel):
    coffee_name: str
    total_quantity: int

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str
    role: str = "employee"

class CoffeeDetails(SQLModel):
    coffee: Coffee
    recipe: Recipe