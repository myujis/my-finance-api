from typing import Any, List
from app.core.config import settings
from fastapi import APIRouter, Depends,HTTPException
from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

from app import schemas
from sqlalchemy.orm import Session, lazyload, joinedload
from app.api import deps
from app import models
import uuid
from pydantic.networks import EmailStr
from app import crud


API_KEY_NAME = "X-API-KEY"
API_KEY = settings.API_KEY

'''
TODO: activate API key at endpoint at end of development
'''

api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
        )



router = APIRouter()





@router.get('/user/{user_id}', response_model=schemas.User_RM)
def get_user(
    *,
    user_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return crud.user.get(db,user_id)

@router.get('/user/email/{user_email}', response_model=schemas.User_RM)
def get_user(
    *,
    user_email: EmailStr,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.User).filter(models.User.email == user_email).first()


@router.post('/user')
def create_user(
    *,
    user:schemas.User,
    db: Session = Depends(deps.get_db)
)->Any:
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete('/user/{user_id}')
def get_user(
    *,
    user_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.User).filter(models.User.id == user_id).delete()


@router.get('/transactions/{transaction_id}')
def get_transaction(
    *,
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.Transactions).filter(models.Transactions.id == transaction_id).first()


@router.get('/transactions/user/{user_email}')
def get_transaction(
    *,
    user_email: EmailStr,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.Transactions)\
        .join(models.Transactions.sub_category, models.Transactions.user)\
        .filter(models.User.email == user_email)\
        .options(joinedload(models.Transactions.sub_category))\
        .all()


@router.post('/transactions')
def create_transaction(
    *,
    transaction: schemas.Transactions,
    db: Session = Depends(deps.get_db)
)->Any:
    db_transaction = models.Transactions(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete('/transactions/{transaction_id}')
def delete_transaction(
    *,
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.Transactions).filter(models.Transactions.id == transaction_id).delete()



@router.get('/category/{category_id}')
def get_category(
    *,
    category_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.Category).filter(models.Category.id == category_id).first()

@router.post('/category')
def create_category(
    *,
    category: schemas.Category,
    db: Session = Depends(deps.get_db)
)->Any:
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete('/category/{category_id}')
def delete_category(
    *,
    category_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.Category).filter(models.Category.id == category_id).delete()


@router.get('/sub_category/{sub_category_id}')
def get_sub_category(
    *,
    sub_category_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.SubCategory).filter(models.SubCategory.id == sub_category_id).first()

@router.post('/sub_category')
def create_sub_category(
    *,
    sub_category: schemas.SubCategory,
    db: Session = Depends(deps.get_db)
)->Any:
    db_sub_category = models.SubCategory(**sub_category.dict())
    db.add(db_sub_category)
    db.commit()
    db.refresh(db_sub_category)
    return db_sub_category

@router.delete('/sub_category/{sub_category_id}')
def delete_category(
    *,
    sub_category_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.SubCategory).filter(models.SubCategory.id == sub_category_id).delete()





@router.get('/settings/{settings_id}')
def get_settings(
    *,
    settings_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.Settings).filter(models.Settings.id == settings_id).first()

@router.post('/settings')
def create_settings(
    *,
    settings: schemas.Settings,
    db: Session = Depends(deps.get_db)
)->Any:
    db_settings = models.Settings(**settings.dict())
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings

@router.delete('/settings/{settings_id}')
def delete_settings(
    *,
    settings_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.Settings).filter(models.Settings.id == settings_id).delete()



@router.get('/settings_association/{settings_association_id}')
def get_settings_association(
    *,
    settings_association_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.SettingsAssociation).filter(models.SettingsAssociation.id == settings_association_id).first()

@router.post('/settings_association')
def create_settings_association(
    *,
    settings_association: schemas.SettingsAssociation,
    db: Session = Depends(deps.get_db)
)->Any:
    #firstly check if association is non existent
    db_settings_association = db.query(models.SettingsAssociation)\
        .filter(models.SettingsAssociation.settings_id == settings_association.settings_id)\
        .filter(models.SettingsAssociation.category_id == settings_association.category_id).first()
    if db_settings_association is not None:
        raise HTTPException(status_code=404, detail="Association already exists")

    #secondly check if we can add the weight desired
    db_settings_association = db.query(models.SettingsAssociation)\
        .filter(models.SettingsAssociation.settings_id == settings_association.settings_id).all()
    
    settings_sum=0
    if len(db_settings_association) != 0:
        for association in db_settings_association:
            settings_sum += association.weight
    
    if settings_sum + settings_association.weight >100:
        raise HTTPException(status_code=500, detail="Not enough percentage to add")


    #proceed with creation

    db_settings_association = models.SettingsAssociation(**settings_association.dict())
    db.add(db_settings_association)
    db.commit()
    db.refresh(db_settings_association)
    return db_settings_association

@router.delete('/settings_association/{settings_association_id}')
def delete_settings_association(
    *,
    settings_association_id: uuid.UUID,
    db: Session = Depends(deps.get_db)
)->Any:
    return db.query(models.SettingsAssociation).filter(models.SettingsAssociation.id == settings_association_id).delete()