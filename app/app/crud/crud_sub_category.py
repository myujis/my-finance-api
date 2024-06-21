from .base import CRUDBase

from app.models.sub_category import SubCategory as SubCategoryModel
from app.schemas.sub_category import SubCategory_Create, SubCategory_Update, SubCategory

sub_category = CRUDBase[SubCategoryModel, SubCategory, SubCategory_Create, SubCategory_Update](SubCategory)