
import datetime
from typing import Optional
import uuid
from pydantic import BaseModel
from .sub_category import SubCategory, SubCategory_RM

class Transactions_Base(BaseModel):
    value: Optional[float]
    date: Optional[datetime.date]
    transaction_type: Optional[str]
    flag_installment: Optional[bool] = False
    installment_quantity: Optional[int] = 0
    user_id: Optional[uuid.UUID]
    sub_category_id: Optional[uuid.UUID]

class Transactions_Create(Transactions_Base):
    pass

class Transactions_Update(Transactions_Base):
    pass

class Transactions_DB(Transactions_Base):
    id: Optional[uuid.UUID]
    
    class Config:
        orm_mode: True

class Transactions(Transactions_DB):
    sub_category: Optional[SubCategory]

    class Config:
        allow_population_by_field_name = True

class Transactions_RM(BaseModel):
    value: float
    date: datetime.date
    transaction_type: str
    flag_installment: bool = False
    installment_quantity: int = 0
    # user_id: uuid.UUID
    # sub_category_id: uuid.UUID
    sub_category: Optional[SubCategory_RM]

    class Config:
        orm_mode=True