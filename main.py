from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from API.user.user import router as User_routes
from user.category import router as Category_routes
from user.subcategory import router as SubCategory_routes
from user.transaction import router as transaction_routes



app = FastAPI()

app.include_router(User_routes, prefix="/users", tags=['Users'])
app.include_router(Category_routes, prefix="/categories", tags=['Categories'])
app.include_router(SubCategory_routes, prefix="/subcategories", tags=['SubCategories'])
app.include_router(transaction_routes, prefix="/transactions", tags=['Transactions'])