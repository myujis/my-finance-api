
from typing import Optional
from pydantic import BaseModel
import uuid

class Category_Base(BaseModel):
    name: Optional[str]
    pass

class Category_Create(Category_Base):
    pass

class Category_Update(Category_Base):
    pass

class Category_DB(Category_Base):
    id: Optional[uuid.UUID]

    class Config:
        orm_mode: True

class Category(Category_DB):

    class Config:
        allow_population_by_field_name = True

class Category_RM(BaseModel):
    name: str
    
    class Config:
        orm_mode=True