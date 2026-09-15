from pydantic import BaseModel, ConfigDict, Field


class BaseCategory(BaseModel):
    model_config = ConfigDict(
        strict=True,
    )

    title: str = Field(
        max_length=55,
    )


class Category(BaseModel):
    id: int


class ReadCategory(BaseCategory):
    pass


class CreateCategory(BaseCategory):
    pass


class UpdateCategory(BaseCategory):
    pass


class DeleteCategory(BaseCategory):
    pass