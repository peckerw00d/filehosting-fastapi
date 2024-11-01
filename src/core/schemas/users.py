from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(..., min_length=3, max_length=15)
    second_name: str = Field(..., min_length=3, max_length=15)
    user_name: str = Field(..., min_length=5, max_length=20)
    email_address: str


class UserRead(UserBase):
    pass


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=16)


class UserUpdate(UserCreate):
    pass
