from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Optional, Sequence, TypeVar

from sqlalchemy import func, select

from fastapi_pagination import Params
from fastapi_pagination.api import create_page, resolve_params
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.ext.sqlalchemy import paginate_query

T = TypeVar("T")


class CustomPage(AbstractPage[T], Generic[T]):
    data: Sequence[T]
    meta: dict
    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ):
        return cls(
            data=items,
            meta={
                "current_page": params.page,
                "per_page": params.size,
                "total_items": total,
            },
        )


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql import Select


async def paginate(
    session: AsyncSession,
    query: Select,
    params: Optional[AbstractParams] = None,
) -> AbstractPage:
    params = resolve_params(params)

    total = await session.scalar(
        select(func.count()).select_from(query.subquery())
    )
    items = await session.execute(paginate_query(query, params))

    return create_page([*items.unique().scalars()], total, params)
