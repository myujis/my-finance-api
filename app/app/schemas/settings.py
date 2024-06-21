
from typing import List, Optional
from pydantic import BaseModel
import uuid

from .settings_association import SettingsAssociation, SettingsAssociation_RM

class Settings_Base(BaseModel):
    user_id: Optional[uuid.UUID]
    pass

class Settings_Create(Settings_Base):
    pass

class Settings_Update(Settings_Base):
    pass

class Settings_DB(Settings_Base):
    id: Optional[uuid.UUID]

    class Config:
        orm_mode: True

class Settings(Settings_DB):
    settings_association: Optional[List[SettingsAssociation]]

    class Config:
        allow_population_by_field_name = True

class Settings_RM(BaseModel):
    # user_id: uuid.UUID
    settings_association: Optional[List[SettingsAssociation_RM]]

    class Config:
        orm_mode=True
