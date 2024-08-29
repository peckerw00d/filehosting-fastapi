from datetime import datetime

from sqlalchemy import DateTime
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column


class FileModel(Base):
    filename: Mapped[str] = mapped_column(index=True)
    path: Mapped[str] = mapped_column(index=True)
    content_type: Mapped[str]
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
