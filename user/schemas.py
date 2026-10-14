from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class prioritylevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class subcategorystatus(str, Enum):
    pending = "pending"
    paid = "paid"
    overdue = "overdue"

class transactiontype(str, Enum):
    income = "income"
    expense = "expense"


# user 
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str   

class UserResponse(UserBase):
    id: str

    class Config:
        from_attributes = True



# category
class CreateCategory(BaseModel):
    categoryName : str
    user_id :str

class CategoryResponse(CreateCategory):
    category_id:str



#subcategory
class CreateSubCategory(BaseModel):
    user_id :str
    category_id:str
    name:str
    amount:float
    priority_level:prioritylevel
    end_date:datetime


class SubCategoryResponse(CreateSubCategory):
    subcategory_id:str
    status:subcategorystatus


class Createtransaction(BaseModel):
    amount: float
    # transactiontype:transactiontype
    discrption:str
    category_id:str
    user_id:str
    subcategory_id:str | None = None

class TransactionResponse(Createtransaction):
    transaction_id:str
    created_at:datetime


