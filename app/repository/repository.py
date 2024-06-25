from typing import Generic, TypeVar
from abc import ABC, abstractmethod
import os
from .exceptions import ModelNotFoundException
import json

T = TypeVar('T')


class RepositoryInterface(Generic[T]):
    def read(self, obj_id: str) -> T:
        pass

    def write(self, obj_id: str, obj: T):
        pass


class AbstractRepository(ABC, RepositoryInterface[T], Generic[T]):
    def __init__(self, path: str):
        self.path = path

    def read(self, obj_id: str) -> T:
        filename = f"{self.path}/{obj_id}.json"
        if not os.path.exists(filename):
            raise ModelNotFoundException()
        with open(filename, 'r') as f:
            return self.unserialize(json.load(f))

    def write(self, obj_id: str, obj: T):
        filename = f"{self.path}/{obj_id}.json"
        with open(filename, 'w') as f:
            json.dump(self.serialize(obj), f)

    @abstractmethod
    def unserialize(self, data: dict) -> T:
        pass

    @abstractmethod
    def serialize(self, obj: T) -> dict:
        pass
