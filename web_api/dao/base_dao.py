from fastapi import HTTPException
from sqlalchemy import text
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from web_api.util.db import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseDao(object):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, session: Session, id: Any) -> Optional[ModelType]:
        filters = [self.model.id == id]
        if 'is_delete' in self.model.__dict__:
            filters.append(self.model.is_delete == 0)
        return session.query(self.model).filter(*filters).first()

    def get_first_obj(self, session: Session, attr_name, attr_value):
        """
        通过字段名称和字段值查找第一条记录
        :param session: session
        :param attr_name: 字段名
        :param attr_value: 字段值
        :return:
        """
        if attr_name not in self.model.__dict__:
            raise HTTPException(500, f'no such attribute: {attr_name}')
        query = session.query(self.model).filter(self.model.__dict__[attr_name] == attr_value)
        if 'is_delete' in self.model.__dict__:
            query = query.filter(self.model.is_delete == 0)
        result = query.first()
        return result

    def get_list(
            self, session: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return session.query(self.model).offset(skip).limit(limit).all()

    def create(self, session: Session, *, obj_in: dict, create_user: int = None, is_commit: bool = True) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        if create_user:
            db_obj.create_user = create_user
        session.add(db_obj)
        if is_commit:
            session.commit()
        else:
            session.flush()
        session.refresh(db_obj)
        return db_obj

    def update(
            self,
            session: Session,
            *,
            db_obj: ModelType,
            obj_in: dict,
            update_user: int = None,
            is_commit: bool = True
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        for field in obj_in:
            if field in obj_data:
                setattr(db_obj, field, obj_in[field])

        if update_user:
            db_obj.update_user = update_user

        if is_commit:
            session.commit()
        else:
            session.flush()
        session.refresh(db_obj)
        return db_obj

    def logically_delete(self, session: Session, id_list: List[int], delete_user: int = None):
        update_info = {'is_delete': 1}
        if delete_user:
            update_info['update_user'] = delete_user

        session.query(self.model).filter(self.model.id.in_(id_list)).update(update_info)
        session.commit()

    def remove(self, session: Session, *, id: int) -> ModelType:
        obj = session.query(self.model).get(id)
        session.delete(obj)
        session.commit()
        return obj

    def check_unique(self, session: Session, key: str, value: Any, id_=None):
        """唯一校验"""
        if key not in self.model.__dict__:
            raise HTTPException(500, f'模型:{self.model.__tablename__} 不存在该字段:{key}')

        return session.query(self.model).filter(
            self.model.__dict__[key] == value,
            self.model.id != id_ if id_ else text(''),
            self.model.is_delete == 0 if 'is_delete' in self.model.__dict__ else text('')
        ).first()

    def query_by_ids(self, session: Session, id_list: List[int]):
        return session.query(self.model).filter(
            self.model.id.in_(id_list),
            self.model.is_delete == 0 if 'is_delete' in self.model.__dict__ else text('')
        ).all()

    def batch_update_by_ids(self, session: Session, id_list: List[int], update_item: dict, is_commit: bool = True):
        session.query(self.model).filter(
            self.model.id.in_(id_list),
            self.model.is_delete == 0 if 'is_delete' in self.model.__dict__ else text('')
        ).update(update_item)
        if is_commit:
            session.commit()
        else:
            session.flush()
