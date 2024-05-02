from abc import ABC, abstractmethod


class BaseHandler(ABC):
    session = None

    @classmethod
    @abstractmethod
    def register(cls, app):
        pass

    @classmethod
    def set_session(cls, session):
        cls.session = session
