from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    password: str
    is_active: bool = True
