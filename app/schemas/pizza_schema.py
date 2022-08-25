from pydantic import BaseModel

from app.enums import Thickness


class PizzaCreate(BaseModel):
    name: str
    thickness: Thickness
    secret_ingredient: str | None

    class Config:
        anystr_strip_whitespace = True


class PizzaUpdate(BaseModel):
    name: str | None
    thickness: Thickness
    secret_ingredient: str | None

    class Config:
        anystr_strip_whitespace = True


class PizzaOut(BaseModel):
    id: int
    name: str
    thickness: Thickness
    secret_ingredient: str | None

    class Config:
        orm_mode = True


