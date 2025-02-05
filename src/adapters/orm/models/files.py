from datetime import datetime
import uuid

from .base import Base
from .users import User, UserStorage

from sqlalchemy import DateTime, Integer, String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FileModel(Base):
    __tablename__ = "files"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    file_url: Mapped[str] = mapped_column(
        String, nullable=False, default=lambda: str(uuid4())
    )
    storage: Mapped["UserStorage"] = relationship(back_populates="files", uselist=False)
    storage_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_storages.id"), nullable=True
    )
