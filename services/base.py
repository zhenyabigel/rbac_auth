from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Executable
from typing import (
    Any,
    List,
    Sequence,
    Type,
)
from models.base import SQLModel
from sqlalchemy import (
    func,
    select,
)
import logging

LOG = logging.getLogger(__name__)


class BaseSession:
    def __init__(self, session: Session):
        self.session = session


class BaseService(BaseSession):
    pass


class BaseDataManager(BaseSession):
    def add_one(self, model: Any) -> None:
        self.session.add(model)

    def add_all(self, models: Sequence[Any]) -> None:
        self.session.add_all(models)

    def get_one(self, stmt: Executable) -> Any:
        return self.session.scalar(statement=stmt)

    def get_all(self, stmt: Executable) -> List[Any]:
        return self.session.scalars(statement=stmt).all()

    def get_from_tvf(self, model: Type[SQLModel], *args: Any) -> List[Any]:
        """Query from table valued function.

        This is a wrapper function that can be used to retrieve data from
        table valued functions.

        Examples:
            from app.models.base import SQLModel

            class MyModel(SQLModel):
                __tablename__ = "function"
                __table_args__ = {"schema": "schema"}

                x: Mapped[int] = mapped_column("x", primary_key=True)
                y: Mapped[str] = mapped_column("y")
                z: Mapped[float] = mapped_column("z")

            # equivalent to "SELECT x, y, z FROM schema.function(1, 'AAA')"
            BaseDataManager(session).get_from_tvf(MyModel, 1, "AAA")
        """

        return self.get_all(self.select_from_tvf(model, *args))

    @staticmethod
    def select_from_tvf(model: Type[SQLModel], *args: Any) -> Executable:
        fn = getattr(getattr(func, model.schema()), model.table_name())
        stmt = select(fn(*args).table_valued(*model.fields()))
        return select(model).from_statement(stmt)
