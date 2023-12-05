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
TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str,
                        user_id: str,
                        expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow()+expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

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

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")

    token = create_access_token(username=user.username,
                                user_id=user.id,
                                expires_delta=TOKEN_EXPIRE_MINUTES)

    return {'access_token': token, 'token_type': 'bearer'}

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate due to username or user_id")
        
        return {'username': username, 'id': user_id} 
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")
