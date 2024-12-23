from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column


class FileModel(Base):
    __tablename__ = "files"

    filename: Mapped[str] = mapped_column(String)
    filesize: Mapped[int] = mapped_column(Integer)
    last_modified: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    etag: Mapped[str] = mapped_column(String)
    content_type: Mapped[str] = mapped_column(String)
