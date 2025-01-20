from sqlalchemy.orm import DeclarativeBase
from typing import List, Dict, Any


class SQLModel(DeclarativeBase):
    @classmethod
    def schema(cls) -> str:
        _schema = cls.__mapper__.selectable.schema
        if _schema is None:
            raise ValueError("Cannot identify model schema")
        return _schema

    @classmethod
    def table_name(cls) -> str:
        return cls.__tablename__

    @classmethod
    def fields(cls) -> List[str]:
        return cls.__mapper__.selectable.c.keys

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        _dict: Dict[str, Any] = dict()
        for key in cls.__mapper__.c.keys():
            _dict[key] = getattr(cls, key)
        return _dict
