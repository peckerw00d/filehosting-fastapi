import datetime

from .base import Base

import uuid

from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, String, DateTime, func, ForeignKey


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    storage: Mapped["UserStorage"] = relationship(back_populates="user", uselist=False)


class UserStorage(Base):
    __tablename__ = "user_storages"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user: Mapped["User"] = relationship(back_populates="storage", uselist=False)
    user_fk: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    bucket_name: Mapped[str] = mapped_column(String)
    files: Mapped["FileModel"] = relationship(back_populates="storage", uselist=True)
