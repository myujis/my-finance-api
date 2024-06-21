
from typing import Optional
import uuid
from pydantic import BaseModel
from .category import Category, Category_RM

class SubCategory_Base(BaseModel):
    name: Optional[str]
    category_id: Optional[uuid.UUID]

class SubCategory_Create(SubCategory_Base):
    pass

class SubCategory_Update(SubCategory_Base):
    pass

class SubCategory_DB(SubCategory_Base):
    id: Optional[uuid.UUID]

    
    class Config:
        orm_mode: True

class SubCategory(SubCategory_DB):
    category: Optional[Category]

    class Config:
        allow_population_by_field_name = True

class SubCategory_RM(BaseModel):
    name: str
    # category_id: uuid.UUID
    
    class Config:
        orm_mode=True