from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from user.schemas import UserBase, UserCreate, UserResponse ,CreateCategory
from Auth.database import get_db


router = APIRouter()


@router.post("/create_user/", response_model= UserResponse)
def create_user(user: UserCreate, db: Session=Depends(get_db) ):
    db_user = user(email=user.email,username=user.username, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/getuser", response_model=UserResponse)
def get_user(email:str, db:Session=Depends(get_db)):
    user = db.user(email = email,)
    print(f" users details {user}")
    return user

