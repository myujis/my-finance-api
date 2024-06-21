from .base import CRUDBase

from app.models.user import User as UserModel
from app.schemas.user import User_Create, User_Update, User

user = CRUDBase[UserModel, User, User_Create, User_Update](UserModel)