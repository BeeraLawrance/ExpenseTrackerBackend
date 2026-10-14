from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user.schemas import UserCreate, UserResponse
from Auth.database import get_db
from user.models import User



router = APIRouter()


@router.post("/create_user/", response_model= UserResponse)
def create_user(user: UserCreate, db: Session=Depends(get_db) ):
    db_user = User(email=user.email,username=user.username, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/getuser", response_model=UserResponse)
def get_user(user_id:str , db:Session=Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    print(f" users details {user}")
    return user

