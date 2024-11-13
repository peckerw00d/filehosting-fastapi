from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=15)
    last_name: str = Field(..., min_length=3, max_length=15)
    user_name: str = Field(..., min_length=5, max_length=20)
    email_address: str


class UserRead(UserBase):
    id: int = Field(...)

    class Config:
        model_config = ConfigDict(
            from_attributes=True
            )


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=30)


class UserUpdate(UserCreate):
    pass
