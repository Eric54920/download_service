import datetime
from typing import Any

import sqlalchemy as sa

from web_api.util.db import Base


class BaseModel(Base):
    """
    基础模型类
    """
    __abstract__ = True

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True, nullable=False)

    def to_dict(self) -> dict:
        item = {}
        for c in self.__table__.columns:
            attr = getattr(self, c.name)
            if isinstance(attr, datetime.datetime):
                attr = int(attr.timestamp())

            item[c.name] = attr
        return item


# class DbHistory(BaseModel):
#     """
#     数据库更新历史, 勿动
#     """
#     __tablename__ = "db_history"
#
#     sql_name = sa.Column(sa.String)
#     content = sa.Column(sa.String)
#     create_time = sa.Column(sa.DateTime, default=datetime.datetime.now)


class CreateMixin(object):
    create_time = sa.Column(sa.DateTime, default=datetime.datetime.now)
    is_delete = sa.Column(sa.Integer, nullable=False, default=0)


class CreateUpdateMixin(CreateMixin):
    update_time = sa.Column(sa.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
