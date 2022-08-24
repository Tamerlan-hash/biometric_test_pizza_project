from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from modules.pagination import Page, paginate
from modules.dal import DAL, get_dal

from app.schemas import RestaurantOut, RestaurantUpdate
from app.models import Restaurant
from app.validator import check_restaurant_exists

restaurant_router = APIRouter(tags=["Restaurant"])


@restaurant_router.get(
    "/restaurants",
    status_code=200,
    response_model=Page[RestaurantOut]
)
async def show_restaurants(
    dal: DAL = Depends(get_dal)
):
    restaurants = await dal.select(
        model=Restaurant
    )
    return await paginate(dal.db_session, restaurants)


@restaurant_router.get(
    "/restaurants/{restaurant_id}",
    status_code=200,
    response_model=RestaurantOut,
    dependencies=[Depends(check_restaurant_exists)]
)
async def show_restaurant_detail(
    restaurant_id: int,
    dal: DAL = Depends(get_dal)
):
    return await dal.get(
        model=Restaurant,
        filters=[Restaurant.id == restaurant_id]
    )


@restaurant_router.patch(
    "/restaurants/{restaurant_id}",
    status_code=202,
    response_model=RestaurantOut,
    dependencies=[Depends(check_restaurant_exists)]
)
async def update_restaurant(
    restaurant_id: int,
    request: RestaurantUpdate,
    dal: DAL = Depends(get_dal)
):
    await dal.update(
        model=Restaurant,
        filters=[Restaurant.id == restaurant_id],
        data=request.dict(exclude_none=True)
    )
    return await dal.get(
        model=Restaurant,
        filters=[Restaurant.id == restaurant_id]
    )


@restaurant_router.delete(
    "/restaurants/{restaurant_id}",
    dependencies=[Depends(check_restaurant_exists)]
)
async def delete_restaurant(
    restaurant_id: int,
    dal: DAL = Depends(get_dal)
):
    await dal.delete(
        model=Restaurant,
        filters=[Restaurant.id == restaurant_id]
    )
    return JSONResponse(
        status_code=200,
        content={"RestaurantDeleted"}
    )
