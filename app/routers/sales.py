from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from datetime import datetime, date, timedelta
from ..database import get_session
from ..models import Sale, SaleRequest, SalesReport, Coffee, Recipe, Milk,StockUpdate , TopSellingItem
from typing import Optional

router = APIRouter()

@router.post("/", response_model=Sale)
def create_sale(sale_request: SaleRequest, session: Session = Depends(get_session)):
    coffee = session.get(Coffee, sale_request.coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    recipe = session.exec(select(Recipe).where(Recipe.coffee_id == sale_request.coffee_id)).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found for this coffee")
    required_coffee = recipe.coffee_grams * sale_request.quantity
    required_milk = recipe.milk_ml * sale_request.quantity
    if coffee.stock_grams < required_coffee:
        raise HTTPException(status_code=400, detail="Not enough coffee in stock")
    milk = session.get(Milk, 1)
    if milk.stock_ml < required_milk:
        raise HTTPException(status_code=400, detail="Not enough milk in stock")
    coffee.stock_grams -= required_coffee
    milk.stock_ml -= required_milk
    total_price = coffee.price * sale_request.quantity
    sale_record = Sale(
        coffee_id=sale_request.coffee_id,
        quantity=sale_request.quantity,
        total_price=total_price,
        sale_date=(datetime.today())
    )
    session.add(sale_record)
    session.add(coffee)
    session.add(milk)
    session.commit()
    session.refresh(sale_record)
    return sale_record

@router.get("/", response_model=List[Sale])
def read_sales(session: Session = Depends(get_session)):
    
    sales = session.exec(select(Sale)).all()
    return sales

@router.get("/reports/daily/", response_model=SalesReport)
def get_daily_report(report_date: date, session: Session = Depends(get_session)):
    
    date_str = report_date.strftime("%Y-%m-%d")
    sales = session.exec(
        select(func.sum(Sale.total_price), func.sum(Sale.quantity))
        .where(Sale.sale_date == date_str)
    ).first()
    total_price, total_quantity = sales if sales and sales[0] else (0.0, 0)
    return SalesReport(
        total_sales=total_price,
        total_quantity=total_quantity
    )

@router.get("/reports/weekly/", response_model=SalesReport)
def get_weekly_report(session: Session = Depends(get_session)):
    
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    sales = session.exec(
        select(func.sum(Sale.total_price), func.sum(Sale.quantity))
        .where(Sale.sale_date >= str(start_date))
    ).first()
    total_price, total_quantity = sales if sales and sales[0] else (0.0, 0)
    return SalesReport(
        total_sales=total_price,
        total_quantity=total_quantity
    )

@router.get("/reports/top-selling/", response_model=List[TopSellingItem])
def get_top_selling_items(session: Session = Depends(get_session)):
    
    results = session.exec(
        select(Coffee.name, func.sum(Sale.quantity))
        .join(Sale, Sale.coffee_id == Coffee.id)
        .group_by(Coffee.id)
        .order_by(func.sum(Sale.quantity).desc())
    ).all()

    top_sellers = []
    for coffee_name, total_quantity in results:
        top_sellers.append(TopSellingItem(coffee_name=coffee_name, total_quantity=total_quantity))

    return top_sellers


@router.put("/milk/stock", response_model=Milk)
def update_milk_stock(stock_update: StockUpdate, session: Session = Depends(get_session)):
    
    milk = session.get(Milk, 1) 
    if not milk:
        raise HTTPException(status_code=404, detail="Milk stock not found")

    milk.stock_ml = stock_update.new_stock
    session.add(milk)
    session.commit()
    session.refresh(milk)
    return milk

@router.get("/reports/range/", response_model=SalesReport)
def get_report_by_date_range(
    start_date: date,
    end_date: date,
    session: Session = Depends(get_session)
):
    
    sales = session.exec(
        select(func.sum(Sale.total_price), func.sum(Sale.quantity))
        .where(Sale.sale_date >= start_date)
        .where(Sale.sale_date <= end_date)
    ).first()

    total_price, total_quantity = sales if sales and sales[0] else (0.0, 0)
    
    return SalesReport(
        total_sales=total_price,
        total_quantity=total_quantity
    )