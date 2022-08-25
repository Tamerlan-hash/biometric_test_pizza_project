from fastapi import Depends, HTTPException, status

from modules.dal import DAL, get_dal

from app.models import Restaurant, Pizza


async def check_restaurant_exists(
    restaurant_id: int,
    dal: DAL = Depends(get_dal)
):
    restaurant = await dal.get(
        model=Restaurant,
        filters=[Restaurant.id == restaurant_id]
    )
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RestaurantDoesNotExistsError"
        )


async def check_restaurant_pizza_exists(
    restaurant_id: int,
    pizza_id: int,
    dal: DAL = Depends(get_dal)
):
    pizza = await dal.get(
        model=Pizza,
        filters=[
            Pizza.id == pizza_id,
            Pizza.restaurant_id == restaurant_id
        ]
    )
    if not pizza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RestaurantPizzaDoesNotExistsError"
        )
