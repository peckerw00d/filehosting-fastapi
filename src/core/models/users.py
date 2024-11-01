from sqlalchemy import String
from core.models.base import Base

from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    user_name: Mapped[str] = mapped_column(String)
    email_address: Mapped[str] = mapped_column(String, unique=True)
    hash_password: Mapped[str] = mapped_column(String)
