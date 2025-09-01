from fastapi import FastAPI
from app.database import create_db_and_tables 
from app.routers import coffees, sales
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from .auth import get_password_hash, create_access_token, verify_password
from .models import User
from sqlmodel import Session, select
from app.database import get_session
from datetime import timedelta
from fastapi import HTTPException, status
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    

@app.get("/")
def read_root():
    return {"message": "Welcome to the Coffee Shop API!"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(coffees.router, prefix="/coffees", tags=["Coffees"])
app.include_router(sales.router, prefix="/sales", tags=["Sales", "Reports"])

