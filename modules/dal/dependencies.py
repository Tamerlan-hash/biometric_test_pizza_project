from settings.database import async_session

from .dal import DAL


async def get_dal():
    async with async_session() as session:
        async with session.begin():
            yield DAL(session)
