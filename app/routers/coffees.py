# app/routers/coffees.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..database import get_session
from ..models import Coffee, CoffeeBase, Recipe, RecipeBase, StockUpdate, CoffeeDetails, User
from ..auth import get_manager_user, get_employee_user

router = APIRouter()

@router.post("/", response_model=Coffee)
def create_coffee(
    coffee: CoffeeBase,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_manager_user)
):
    """
    Yeni bir kahve türü ekler ve başlangıç stoğunu kaydeder. (Yönetici yetkisi gerektirir)
    """
    db_coffee = Coffee.model_validate(coffee)
    session.add(db_coffee)
    session.commit()
    session.refresh(db_coffee)
    return db_coffee

@router.get("/", response_model=List[Coffee])
def read_coffees(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_employee_user)
):
    """
    Tüm kahve türlerini listeler. (Çalışan yetkisi gerektirir)
    """
    coffees = session.exec(select(Coffee)).all()
    return coffees

@router.post("/recipes/", response_model=Recipe)
def create_recipe(
    recipe: RecipeBase,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_manager_user)
):
    """
    Yeni bir kahve tarifi ekler. (Yönetici yetkisi gerektirir)
    """
    db_recipe = Recipe.model_validate(recipe)
    
    coffee = session.get(Coffee, db_recipe.coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    return db_recipe

@router.get("/recipes/", response_model=List[Recipe])
def read_recipes(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_employee_user)
):
    """
    Tüm kahve tariflerini listeler. (Çalışan yetkisi gerektirir)
    """
    recipes = session.exec(select(Recipe)).all()
    return recipes

@router.get("/{coffee_id}/details", response_model=CoffeeDetails)
def get_coffee_details(
    coffee_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_employee_user)
):
    """
    Belirli bir kahvenin tüm detaylarını (tarifi dahil) döndürür. (Çalışan yetkisi gerektirir)
    """
    coffee = session.get(Coffee, coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
        
    recipe = session.exec(
        select(Recipe).where(Recipe.coffee_id == coffee_id)
    ).first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found for this coffee")

    return CoffeeDetails(coffee=coffee, recipe=recipe)

@router.put("/{coffee_id}/stock", response_model=Coffee)
def update_coffee_stock(
    coffee_id: int,
    stock_update: StockUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_manager_user)
):
    """
    Belirli bir kahvenin stok miktarını günceller. (Yönetici yetkisi gerektirir)
    """
    coffee = session.get(Coffee, coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    coffee.stock_grams = stock_update.new_stock
    session.add(coffee)
    session.commit()
    session.refresh(coffee)
    return coffee

@router.put("/{coffee_id}", response_model=Coffee)
def update_coffee(
    coffee_id: int,
    coffee: CoffeeBase,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_manager_user)
):
    """
    Belirli bir kahve kaydını günceller. (Yönetici yetkisi gerektirir)
    """
    db_coffee = session.get(Coffee, coffee_id)
    if not db_coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    coffee_data = coffee.model_dump(exclude_unset=True)
    db_coffee.sqlmodel_update(coffee_data)
    session.add(db_coffee)
    session.commit()
    session.refresh(db_coffee)
    return db_coffee

@router.delete("/{coffee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coffee(
    coffee_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_manager_user)
):
    """
    Belirli bir kahve kaydını siler. (Yönetici yetkisi gerektirir)
    """
    coffee = session.get(Coffee, coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    session.delete(coffee)
    session.commit()
    return {"ok": True}

@router.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(
    recipe_id: int,
    recipe: RecipeBase,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_manager_user)
):
    """
    Belirli bir tarifi günceller. (Yönetici yetkisi gerektirir)
    """
    db_recipe = session.get(Recipe, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe_data = recipe.model_dump(exclude_unset=True)
    db_recipe.sqlmodel_update(recipe_data)
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    return db_recipe

@router.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_manager_user)
):
    """
    Belirli bir tarifi siler. (Yönetici yetkisi gerektirir)
    """
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    session.delete(recipe)
    session.commit()
    return {"ok": True}