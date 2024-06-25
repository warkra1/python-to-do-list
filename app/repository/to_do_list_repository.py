import os

from .repository import AbstractRepository, T
from app.models.to_do_item import ToDoItem
from app.models.to_do_list import ToDoList


class ToDoListRepository(AbstractRepository[ToDoList]):
    def serialize(self, obj: ToDoList) -> dict:
        items = []
        for item in obj.items:
            items.append({"title": item.title})
        return {"items": items}

    def unserialize(self, data: dict) -> ToDoList:
        items = []
        for item in data["items"]:
            items.append(ToDoItem(item["title"]))
        return ToDoList(items)


to_do_list_repository = ToDoListRepository(os.getcwd() + "/data/lists")
