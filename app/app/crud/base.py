from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import uuid
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base

from sqlalchemy import exc

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType,SchemaType,CreateSchemaType,UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: uuid.UUID) -> [ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType)-> ModelType:
        obj_in_data = jsonable_encoder(obj_in)

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        try:
            db.commit()
        except exc.SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f'Error creating object {e.orig}')
        db.refresh()
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str,Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict()
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)

        try:
            db.commit()
        except exc.SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f'Error updating object {e.orig}')

        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: uuid.UUID) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)

        try:
            db.commit()
        except exc.SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f'Error deleting object {e.orig}')
        return obj
