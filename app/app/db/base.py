# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.category import Category
from app.models.sub_category import SubCategory
from app.models.settings import Settings
from app.models.settings_association import SettingsAssociation
from app.models.user import User
from app.models.transactions import Transactions