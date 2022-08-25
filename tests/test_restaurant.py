import pytest

from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Restaurant


@pytest.mark.asyncio
async def test_create_restaurant(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict
):
    payload = test_restaurant_data["case_create"]["payload"]
    response = await async_client.post("/restaurants", json=payload)

    assert response.status_code == 201

    got = response.json()
    want = test_restaurant_data["case_create"]["want"]

    for key, value in want.items():
        assert got[key] == value

    statement = select(Restaurant).where(Restaurant.id == got["id"])
    results = await async_session.execute(statement=statement)
    restaurant = results.scalar_one()

    for key, value in want.items():
        assert getattr(restaurant, key) == value


@pytest.mark.asyncio
async def test_get_restaurants_in_pagination(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict
):
    data = test_restaurant_data["initial_data"]["restaurant"]
    statement = insert(Restaurant).values(data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    data = test_restaurant_data["initial_data"]["additional_restaurant"]
    statement = insert(Restaurant).values(data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.get(
        "/restaurants",
        params={"page": 1, "size": 50}
    )
    assert response.status_code == 200

    got = response.json()['data']
    want = test_restaurant_data["case_get_pagination"]["want"]

    assert got == want


@pytest.mark.asyncio
async def test_get_restaurant_detail(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict
):
    data = test_restaurant_data["initial_data"]["restaurant"]
    statement = insert(Restaurant).values(data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.get(f"/restaurants/{data['id']}")
    assert response.status_code == 200

    got = response.json()
    want = test_restaurant_data["case_get"]["want"]

    for key, value in want.items():
        assert got[key] == value


@pytest.mark.asyncio
async def test_patch_restaurant(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict
):
    data = test_restaurant_data["initial_data"]["restaurant"]
    statement = insert(Restaurant).values(data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    payload = test_restaurant_data["case_patch"]["payload"]
    response = await async_client.patch(
        f"/restaurants/{data['id']}",
        json=payload
    )
    assert response.status_code == 202

    got = response.json()
    want = test_restaurant_data["case_patch"]["want"]

    for key, value in want.items():
        assert got[key] == value


@pytest.mark.asyncio
async def test_delete_restaurant(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_restaurant_data: dict
):
    data = test_restaurant_data["initial_data"]["restaurant"]
    statement = insert(Restaurant).values(data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.delete(f"/restaurants/{data['id']}")
    assert response.status_code == 200

    got = response.json()
    want = test_restaurant_data["case_delete"]["want"]

    assert got == want["message"]

    statement = select(
        Restaurant
    ).where(
        Restaurant.id == data["id"]
    )
    results = await async_session.execute(statement=statement)
    restaurant = results.scalar_one_or_none()

    assert restaurant is None
