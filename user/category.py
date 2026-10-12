from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user.schemas import UserBase, UserCreate, UserResponse ,CreateCategory
from Auth.database import get_db

router = APIRouter()

@router.post("/create_category/")
def create_category(category:CreateCategory, db:Session=Depends(get_db)):
    db_category = category(categoryName=category.categoryName, user_id=category.user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get('/get_category/')
def get_category(category_id:str, db:Session=Depends(get_db)):
    if category_id:
        category = db.query(category).filter(category_id==category_id).first()
    elif not category_id:
        raise HTTPException(status_code=400, detail="Category ID is required")
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

