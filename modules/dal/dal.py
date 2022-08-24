from sqlalchemy import delete, exists, insert, update
from sqlalchemy.future import select

from settings.database.mixin import SessionMixin


class DAL(SessionMixin):
    """
    В классе хранятся абстрактные и асинхорнные методы вызовов ORM
    """

    async def is_exists(self, model, options=None, select_from=None,
                        joins=None, filters=None):
        """
        Возвращает логическое значение, указывающее,
        существует ли запись в базе данных.

        :param model: Модель для выбора
        :param options: список параметров, которые будут переданы в запрос
        :param select_from: Это предложение FROM запроса
        :param joins: список объединений, применяемых к запросу
        :param filters: список фильтров для применения к запросу
        :return: Первый объект.
        """

        select_objects = await self.select(
            model=model,
            options=options,
            select_from=select_from,
            joins=joins,
            filters=filters
        )
        q = await self.db_session.execute(
            exists(select_objects).select()
        )
        return q.scalars().first()

    async def create(self, model, data):
        """
        Он создает новый объект типа модели, добавляет его в сеанс базы данных,
        а затем сбрасывает сеанс, чтобы зафиксировать изменения в базе данных.

        :param model: Класс модели, для которого вы хотите создать новый объект
        :param data: Данные для вставки в базу данных
        :return: Новый созданный объект.
        """
        new_object = model(**data)
        self.db_session.add(new_object)
        await self.db_session.flush()
        return new_object

    async def select(self, model, options=None, select_from=None,
                     joins=None, filters=None, order_by=None):
        """
        Он принимает модель, отношения, выборку из, объединения и фильтры, и
        возвращает объект запроса.

        :param model: Модель для выбора
        :param options: список параметров, которые будут переданы в запрос
        :param select_from: Это предложение FROM запроса
        :param joins: список объединений, применяемых к запросу
        :param filters: список фильтров для применения к запросу
        :return: Объект запроса.
        """

        q = select(model)
        if options:
            q = q.options(*options)
        if select_from:
            q = q.select_from(select_from)
        if joins:
            q = q.join(joins)
        if filters:
            q = q.filter(*filters)
        if order_by:
            q = q.order_by(*order_by)
        return q

    async def get_all(self, model=None, options=None, select_from=None,
                      joins=None, filters=None, order_by=None):
        """
        Он принимает модель, отношения, выборку из, объединения и фильтры, и
        возвращает список всех результатов из базы данных.

        :param model: Модель для выбора
        :param options: список параметров, которые будут переданы в запрос
        :param select_from: Это предложение FROM запроса
        :param joins: список объединений, применяемых к запросу
        :param filters: список фильтров для применения к запросу
        :return: Список всех объектов в базе данных.
        """
        select_objects = await self.select(
            model=model,
            options=options,
            select_from=select_from,
            joins=joins,
            filters=filters,
            order_by=order_by
        )
        q = await self.db_session.execute(select_objects)
        return q.scalars().all()

    async def get(self, model, options=None, select_from=None,
                  joins=None, filters=None, order_by=None):
        """
        Возвращает первый результат запроса

        :param model: Модель для выбора
        :param options: список параметров, которые будут переданы в запрос
        :param select_from: Это предложение FROM запроса
        :param joins: список объединений, применяемых к запросу
        :param filters: список фильтров для применения к запросу
        :return: Первый объект.
        """
        select_objects = await self.select(
            model=model,
            options=options,
            select_from=select_from,
            joins=joins,
            filters=filters,
            order_by=order_by
        )
        q = await self.db_session.execute(select_objects)
        return q.scalars().first()

    async def insert(self, model, data):
        """
        Он вставляет данные в базу данных

        :param model: Имя таблицы
        :param data: Данные для вставки в таблицу
        """
        await self.db_session.execute(insert(model).values(data))

    async def update(self, model, filters, data):
        """
        Он обновляет модель данными и возвращает обновленную модель.

        :param model: Модель для обновления
        :param data: словарь данных, которые вы хотите обновить
        :param filters: список фильтров для применения к запросу
        :return: Обновленный объект.
        """
        q = update(model).filter(*filters)
        q = q.values(data)
        q = q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def delete(self, model, filters):
        """
        Он удаляет строку из таблицы базы данных, соответствующую переданному

        классу модели, где переданные фильтры верны.
        :param model: Модель, из которой нужно удалить
        :param filters: список выражений фильтра
        """
        await self.db_session.execute(delete(model).filter(*filters))

    async def get_or_create(self, model, filters, data):
        """
        Если объект не существует, создайте его. Если да, то верни

        :param model: Модель, используемая для запроса
        :param filters: Словарь фильтров для применения к запросу
        :param data: Данные для вставки в базу данных
        :return: Объект возвращается.
        """
        obj = await self.get(
            model=model,
            filters=filters
        )
        if not obj:
            obj = await self.create(model, data)
        return obj

    async def create_or_update(self, model, filters=None,
                               update_data=None, create_data=None):
        obj = await self.get(
            model=model,
            filters=filters
        )
        if obj:
            await self.update(
                model=model,
                filters=filters,
                data=update_data,
            )
        else:
            await self.create(
                model=model,
                data=create_data
            )
