from .base import CRUDBase

from app.models.category import Category as CategoryModel
from app.schemas.category import Category_Create, Category_Update, Category

category = CRUDBase[CategoryModel, Category, Category_Create, Category_Update](Category)