from training_projects.rbac_auth.models.base import SQLModel
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(SQLModel):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    email: Mapped[str] = mapped_column("email", primary_key=True)
    name: Mapped[str] = mapped_column("name")
    role: Mapped[str] = mapped_column("role")
    hashed_password: Mapped[str] = mapped_column("hashed_password")
