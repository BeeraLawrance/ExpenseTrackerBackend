from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user.schemas import Createtransaction, TransactionResponse, transactiontype
from Auth.database import get_db
from user.models import transaction


router = APIRouter()

@router.post("/transactions",)
def create_transaction(transaction_data: Createtransaction,transactiontype:transactiontype, db: Session = Depends(get_db)):
    new_transaction = transaction(
        amount=transaction_data.amount,
        category_id=transaction_data.category_id,
        subcategory_id=transaction_data.subcategory_id ,
        user_id=transaction_data.user_id,
        transaction_type=transactiontype.value,
        discrption=transaction_data.discrption
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.get("/transactions/{transaction_id}", )
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    transaction_item = db.query(transaction).filter(transaction.id == transaction_id).first()
    if not transaction_item:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction_item