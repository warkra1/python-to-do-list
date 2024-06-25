import os
from abc import ABC

from .repository import AbstractRepository, T
from app.models.user import User
from .exceptions import ModelNotFoundException


class UserRepository(AbstractRepository[User], ABC):
    def unserialize(self, data: dict) -> User:
        return User(data['login'], data['password'])

    def serialize(self, obj: User) -> dict:
        return {"login": obj.login, "password": obj.password}


user_repository = UserRepository(os.getcwd() + "/data/users")
