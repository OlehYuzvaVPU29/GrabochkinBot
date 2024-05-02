from sqlalchemy import Column, Integer, String

from models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, unique=True)
    email = Column(String, unique=True)
