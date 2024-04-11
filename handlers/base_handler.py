from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @classmethod
    @abstractmethod
    def register(cls, app):
        pass
