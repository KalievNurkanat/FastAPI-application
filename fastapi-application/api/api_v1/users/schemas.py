from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUser(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: EmailStr | None = None
    password: str 
    is_active: bool = True
    


class ReadUser(CreateUser):
    pass