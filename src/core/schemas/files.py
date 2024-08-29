from datetime import datetime
from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    filename: str
    path: str
    content_type: str

class FileCreate(FileBase):
    pass

class FileResponse(FileBase):
    id: int
    uploaded_at: datetime

    class Config:
        model_config = ConfigDict(
            from_attributes=True,
        )
        