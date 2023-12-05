from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from database import SessionLocal
import starlette.status as status
from .auth import get_current_user


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not get access")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    
    db.add(todo_model)
    db.commit()