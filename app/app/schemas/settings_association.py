
from typing import Optional
from pydantic import BaseModel
import uuid
from .category import Category, Category_RM

class SettingsAssociation_Base(BaseModel):
    weight: Optional[float]
    settings_id: Optional[uuid.UUID]
    category_id: Optional[uuid.UUID]
    pass

class SettingsAssociation_Create(SettingsAssociation_Base):
    pass

class SettingsAssociation_Update(SettingsAssociation_Base):
    pass

class SettingsAssociation_DB(SettingsAssociation_Base):
    id: Optional[uuid.UUID]
    
    class Config:
        orm_mode: True

class SettingsAssociation(SettingsAssociation_DB):
    category: Optional[Category]

    class Config:
        allow_population_by_field_name = True

class SettingsAssociation_RM(BaseModel):
    weight: int
    # settings_id: uuid.UUID
    # category_id: uuid.UUID
    category: Optional[Category_RM]
    
    class Config:
        orm_mode=True