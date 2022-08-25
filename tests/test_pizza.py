import pytest

from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Restaurant, Pizza


@pytest.mark.asyncio
async def test_create_restaurant_pizza(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict,
    test_pizza_data: dict
):
    restaurant_data = test_restaurant_data["initial_data"]["restaurant"]
    statement = insert(Restaurant).values(restaurant_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    payload = test_pizza_data["case_create"]["payload"]
    response = await async_client.post(
        f"/restaurants/{restaurant_data['id']}/pizzas",
        json=payload
    )

    assert response.status_code == 201

    got = response.json()
    want = test_pizza_data["case_create"]["want"]

    for key, value in want.items():
        assert got[key] == value

    statement = select(Pizza).where(
        Pizza.id == got["id"],
        Pizza.restaurant_id == got["restaurant_id"]
    )
    results = await async_session.execute(statement=statement)
    pizza = results.scalar_one()

    for key, value in want.items():
        assert getattr(pizza, key) == value


@pytest.mark.asyncio
async def test_get_restaurant_pizzas_in_pagination(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict,
    test_pizza_data: dict
):
    restaurant_data = test_restaurant_data["initial_data"]["restaurant"]
    statement = insert(Restaurant).values(restaurant_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    pizza_data = test_pizza_data["initial_data"]["pizza"]
    statement = insert(Pizza).values(pizza_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    pizza_data = test_pizza_data["initial_data"]["additional_pizza"]
    statement = insert(Pizza).values(pizza_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.get(
        f"/restaurants/{restaurant_data['id']}/pizzas",
        params={"page": 1, "size": 50}
    )
    assert response.status_code == 200

    got = response.json()['data']
    want = test_pizza_data["case_get_pagination"]["want"]

    assert got == want


@pytest.mark.asyncio
async def test_get_restaurant_pizza_detail(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict,
    test_pizza_data: dict
):
    restaurant_data = test_restaurant_data["initial_data"]["restaurant"]
    statement = insert(Restaurant).values(restaurant_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    pizza_data = test_pizza_data["initial_data"]["pizza"]
    statement = insert(Pizza).values(pizza_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.get(
        f"/restaurants/{restaurant_data['id']}/pizzas/{pizza_data['id']}"
    )
    assert response.status_code == 200

    got = response.json()
    want = test_pizza_data["case_get"]["want"]

    for key, value in want.items():
        assert got[key] == value


@pytest.mark.asyncio
async def test_patch_restaurant_pizza(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict,
    test_pizza_data: dict
):
    restaurant_data = test_restaurant_data["initial_data"]["restaurant"]
    statement = insert(Restaurant).values(restaurant_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    pizza_data = test_pizza_data["initial_data"]["pizza"]
    statement = insert(Pizza).values(pizza_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    payload = test_pizza_data["case_patch"]["payload"]
    response = await async_client.patch(
        f"/restaurants/{restaurant_data['id']}/pizzas/{pizza_data['id']}",
        json=payload
    )
    assert response.status_code == 202

    got = response.json()
    want = test_pizza_data["case_patch"]["want"]

    for key, value in want.items():
        assert got[key] == value


@pytest.mark.asyncio
async def test_delete_restaurant_pizza(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict,
    test_pizza_data: dict
):
    restaurant_data = test_restaurant_data["initial_data"]["restaurant"]
    statement = insert(Restaurant).values(restaurant_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    pizza_data = test_pizza_data["initial_data"]["pizza"]
    statement = insert(Pizza).values(pizza_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.delete(
        f"/restaurants/{restaurant_data['id']}/pizzas/{pizza_data['id']}"
    )
    assert response.status_code == 200

    got = response.json()
    want = test_pizza_data["case_delete"]["want"]

    assert got == want["message"]

    statement = select(
        Pizza
    ).where(
        Pizza.restaurant_id == restaurant_data["id"],
        Pizza.id == pizza_data["id"]
    )
    results = await async_session.execute(statement=statement)
    pizza = results.scalar_one_or_none()

    assert pizza is None
