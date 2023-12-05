from datetime import datetime, timedelta
from typing import Union
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing_extensions import Annotated

from fastapi import APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '6a395a58a034184bea5e5e76334afa7afb8242c5acd5c56afd4387d232097c27'
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = 30 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

@router.get("/get_users", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    users = db.query(Users).all()
    if users is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request while getting all users.") 
    return users

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )

    db.add(create_user_model)
    db.commit()