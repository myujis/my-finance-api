from .base import CRUDBase

from app.models.settings import Settings as SettingsModel
from app.schemas.settings import Settings_Create, Settings_Update, Settings

settings = CRUDBase[SettingsModel, Settings, Settings_Create, Settings_Update](Settings)