from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user.schemas import Createtransaction, TransactionResponse
from Auth.database import get_db
from user.models import transaction


router = APIRouter()

@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(transaction_data: Createtransaction, db: Session = Depends(get_db)):
    new_transaction = transaction(
        amount=transaction_data.amount,
        category_id=transaction_data.catergory_id,
        subcategory_id=transaction_data.subcategory_id,
        user_id=transaction_data.user_id,
        transaction_type=transaction_data.transactiontype.value,
        discrption=transaction_data.description
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction