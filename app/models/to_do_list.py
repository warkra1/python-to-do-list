from typing import List
from .to_do_item import ToDoItem


class ToDoList:
    def __init__(self, items: List[ToDoItem]):
        self.items = items
