from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user.schemas import CreateCategory
from Auth.database import get_db
from user.models import category

router = APIRouter()

@router.post("/create_category/")
def create_category(category_items:CreateCategory, db:Session=Depends(get_db)):
    db_category = category(name=category_items.categoryName, user_id=category_items.user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get('/get_category/')
def get_category(category_id:str, db:Session=Depends(get_db)):
    if not category_id:
        raise HTTPException(status_code=400, detail="Category ID is required")
    category_item = db.query(category).filter(category.id == category_id).first()
    if not category_item:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category_item

