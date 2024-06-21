
from typing import List, Optional
import uuid
from pydantic import BaseModel, EmailStr
from .transactions import Transactions, Transactions_RM
from .settings import Settings, Settings_RM

class User_Base(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]

class User_Create(User_Base):
    pass

class User_Update(User_Base):
    pass

class User_DB(User_Base):
    id: Optional[uuid.UUID]
    
    class Config:
        orm_mode: True

class User(User_DB):
    transactions: Optional[List[Transactions]]
    settings: Optional[List[Settings]]

    class Config:
        orm_mode: True

class User_RM(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    transactions: Optional[List[Transactions_RM]]
    settings: Optional[List[Settings_RM]]

    class Config:
        orm_mode=True

