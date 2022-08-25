from pydantic import BaseModel

from app.enums import Thickness, Cheese


class PizzaCreate(BaseModel):
    name: str
    cheese: Cheese
    thickness: Thickness
    secret_ingredient: str | None

    class Config:
        anystr_strip_whitespace = True


class PizzaUpdate(BaseModel):
    restaurant_id: int | None
    name: str | None
    cheese: Cheese | None
    thickness: Thickness | None
    secret_ingredient: str | None

    class Config:
        anystr_strip_whitespace = True


class PizzaOut(BaseModel):
    id: int
    restaurant_id: int
    name: str
    cheese: Cheese
    thickness: Thickness
    secret_ingredient: str | None

    class Config:
        orm_mode = True


