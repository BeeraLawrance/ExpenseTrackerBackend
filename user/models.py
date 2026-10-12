from sqlalchemy import Column, String, ForeignKey,DateTime,Float
from sqlalchemy.sql import func
from Auth.database import Base
from user.schemas import prioritylevel,subcategorystatus,transactiontype
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True , default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()

    )

class category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)

class subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    amount = Column(Float, nullable=False)
    category_id = Column(String, ForeignKey('categories.id'))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    priority_level= Column(String, default=prioritylevel.low.value)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default=subcategorystatus.pending.value)


class transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    amount = Column(Float, nullable=False)
    category_id = Column(String, ForeignKey('categories.id'))
    subcategory_id = Column(String, ForeignKey('subcategories.id'),nullable=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime,nullable=False, server_default=func.now())
    transaction_type = Column(String, default=transactiontype.expense.value) 
    discrption = Column(String, nullable=True)
    