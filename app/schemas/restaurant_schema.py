from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    address: str

    class Config:
        anystr_strip_whitespace = True


class RestaurantUpdate(BaseModel):
    name: str | None
    address: str | None

    class Config:
        anystr_strip_whitespace = True


class RestaurantOut(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        orm_mode = True
