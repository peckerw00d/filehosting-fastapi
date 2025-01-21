from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Integer, String
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column


class FileModel(Base):
    __tablename__ = "files"

    file_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=lambda: str(uuid4()),
    )
