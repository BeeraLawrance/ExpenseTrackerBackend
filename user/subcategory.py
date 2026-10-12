from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session 
from user.schemas import CreateSubCategory
from Auth.database import get_db


router = APIRouter()

@router.post("/create_subcategory/")
def create_subcategory(subcategory:CreateSubCategory, db:Session=Depends(get_db)):
    db_subcategory = subcategory(subcategoryName=subcategory.subcategoryName, category_id=subcategory.category_id)
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

@router.get('/get_subcategory/')
def get_subcategory(subcategory_id:str, db:Session=Depends(get_db)):
    if subcategory_id:
        subcategory = db.query(subcategory).filter(subcategory_id==subcategory_id).first()
    elif not subcategory_id:
        raise HTTPException(status_code=400, detail="SubCategory ID is required")
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    
    return subcategory