from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from modules.pagination import Page, paginate
from modules.dal import DAL, get_dal

from app.schemas import PizzaOut, PizzaUpdate, PizzaCreate
from app.models import Pizza
from app.validator import (
    check_restaurant_exists,
    check_restaurant_pizza_exists
)

pizza_router = APIRouter(tags=["Pizza"])


@pizza_router.post(
    "/restaurants/{restaurant_id}/pizzas",
    status_code=201,
    response_model=PizzaOut,
    dependencies=[Depends(check_restaurant_exists)]
)
async def create_restaurant_pizzas(
    restaurant_id: int,
    request: PizzaCreate,
    dal: DAL = Depends(get_dal)
):
    data = request.dict()
    data["restaurant_id"] = restaurant_id
    pizza = await dal.create(
        model=Pizza,
        data=data
    )
    return await dal.get(
        model=Pizza,
        filters=[
            Pizza.id == pizza.id,
        ]
    )


@pizza_router.get(
    "/restaurants/{restaurant_id}/pizzas",
    status_code=200,
    response_model=Page[PizzaOut],
    dependencies=[Depends(check_restaurant_exists)]
)
async def show_restaurant_pizzas(
    restaurant_id: int,
    dal: DAL = Depends(get_dal)
):
    pizzas = await dal.select(
        model=Pizza,
        filters=[Pizza.restaurant_id == restaurant_id]
    )
    return await paginate(dal.db_session, pizzas)


@pizza_router.get(
    "/restaurants/{restaurant_id}/pizzas/{pizza_id}",
    status_code=200,
    response_model=PizzaOut,
    dependencies=[
        Depends(check_restaurant_exists),
        Depends(check_restaurant_pizza_exists)
    ]
)
async def show_restaurant_pizza_detail(
    restaurant_id: int,
    pizza_id: int,
    dal: DAL = Depends(get_dal)
):
    return await dal.get(
        model=Pizza,
        filters=[
            Pizza.restaurant_id == restaurant_id,
            Pizza.id == pizza_id
        ]
    )


@pizza_router.patch(
    "/restaurants/{restaurant_id}/pizzas/{pizza_id}",
    status_code=202,
    response_model=PizzaOut,
    dependencies=[
        Depends(check_restaurant_exists),
        Depends(check_restaurant_pizza_exists)
    ]
)
async def update_restaurant_pizza(
    restaurant_id: int,
    pizza_id: int,
    request: PizzaUpdate,
    dal: DAL = Depends(get_dal)
):
    await dal.update(
        model=Pizza,
        filters=[
            Pizza.restaurant_id == restaurant_id,
            Pizza.id == pizza_id
        ],
        data=request.dict(exclude_none=True)
    )
    return await dal.get(
        model=Pizza,
        filters=[
            Pizza.restaurant_id == restaurant_id,
            Pizza.id == pizza_id
        ]
    )


@pizza_router.delete(
    "/restaurants/{restaurant_id}/pizzas/{pizza_id}",
    dependencies=[
        Depends(check_restaurant_exists),
        Depends(check_restaurant_pizza_exists)
    ]
)
async def delete_restaurant_pizza(
    restaurant_id: int,
    pizza_id: int,
    dal: DAL = Depends(get_dal)
):
    await dal.delete(
        model=Pizza,
        filters=[
            Pizza.restaurant_id == restaurant_id,
            Pizza.id == pizza_id
        ]
    )
    return JSONResponse(
        status_code=200,
        content={"detail": "RestaurantPizzaDeleted"}
    )