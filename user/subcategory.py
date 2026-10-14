from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session 
from user.schemas import CreateSubCategory,subcategorystatus
from Auth.database import get_db
from user.models import subcategory
from user.models import transaction



router = APIRouter()

@router.post("/create_subcategory/")
def create_subcategory(subcategory_items:CreateSubCategory, db:Session=Depends(get_db)):
    print(subcategory_items.end_date )
    db_subcategory = subcategory(
                                 user_id=subcategory_items.user_id,
                                 category_id=subcategory_items.category_id, 
                                 name=subcategory_items.name, 
                                 amount=subcategory_items.amount,
                                 priority_level=subcategory_items.priority_level,
                                 end_date=subcategory_items.end_date)
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

@router.get('/get_subcategory/')
def get_subcategory(subcategory_id:str,db:Session=Depends(get_db)):
    if not subcategory_id:
        raise HTTPException(status_code=400, detail="SubCategory ID is required")
    subcategories = db.query(subcategory).filter(subcategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return subcategories


@router.get('/get_subcategories_by_category/')
def get_subcategories_by_category(category_id:str,db:Session=Depends(get_db)):
    if not category_id:
        raise HTTPException(status_code=400, detail="Category ID is required")
    subcategories = db.query(subcategory).filter(subcategory.category_id == category_id).all()
    if not subcategories:
        raise HTTPException(status_code=404, detail="No SubCategories found for this Category")
    return subcategories


@router.get('/set_status/')
def set_status(subcategory_id:str,subcategorystatus:subcategorystatus, db:Session=Depends(get_db)):
    if not subcategory_id:
        raise HTTPException(status_code=400, detail="SubCategory ID is required")
    
    subcategory_item = db.query(subcategory).filter(subcategory.id == subcategory_id).first()
    if not subcategory_item:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    
    if subcategorystatus.value == "paid" and subcategory_item.status != "paid":
        subcategory_item.status = "paid"
        new_transaction = transaction(
            amount=subcategory_item.amount,
            category_id=subcategory_item.category_id,
            subcategory_id=subcategory_item.id ,
            user_id=subcategory_item.user_id,
            transaction_type="expense",
            discrption=f"Payment for subcategory {subcategory_item.name}"
        )
        db.add(new_transaction)
    elif subcategorystatus.value == "pending" and subcategory_item.status != "pending":
        db.query(transaction).filter(transaction.subcategory_id == subcategory_id).delete()

    db.commit()
    return HTTPException(status_code=200, detail=f"SubCategory status updated to {subcategorystatus.value}")

