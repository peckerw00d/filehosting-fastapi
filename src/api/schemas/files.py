from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class FileBase(BaseModel):
    filename: str = Field(..., description="Имя файла")
    # file_url: str = Field(..., description="Ссылка на файл")
    file_size: int = Field(..., description="Размер файла в байтах")
    last_modified: datetime = Field(
        ..., description="Дата и время последнего изменения"
    )
    etag: str = Field(..., description="ETag файла")
    content_type: str = Field(..., description="Тип файла")


class FileCreate(FileBase):
    pass


class FileResponse(FileBase):
    class Config:
        model_config = ConfigDict(
            from_attributes=True,
        )
