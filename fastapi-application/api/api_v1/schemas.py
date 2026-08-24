from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    age: int


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    pass