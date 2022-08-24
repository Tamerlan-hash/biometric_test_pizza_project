from .connection import async_session


class SessionMixin:
    def __init__(self, db_session: async_session):
        self.db_session = db_session
