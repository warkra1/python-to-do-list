from app.repository.to_do_list_repository import ToDoListRepository, to_do_list_repository
from app.repository.repository import RepositoryInterface
from app.models.user import User
from app.models.to_do_list import ToDoList
from app.repository.exceptions import ModelNotFoundException
from app.models.to_do_item import ToDoItem


class ToDoListService:
    def __init__(self, repository: RepositoryInterface[ToDoList]):
        self.repository = repository

    def get_list(self, user: User) -> ToDoList:
        try:
            return self.repository.read(user.login)
        except ModelNotFoundException:
            return self.__create_list(user)

    def create_item(self, user: User, item: ToDoItem, number: int) -> ToDoList:
        to_do_list = self.get_list(user)
        if number > len(to_do_list.items):
            number = len(to_do_list.items)
        to_do_list.items.insert(number, item)
        self.repository.write(user.login, to_do_list)
        return to_do_list

    def update_item(self, user: User, item: ToDoItem, number: int) -> ToDoList:
        to_do_list = self.get_list(user)
        if number < len(to_do_list.items):
            to_do_list.items[number] = item
        self.repository.write(user.login, to_do_list)
        return to_do_list

    def delete_item(self, user: User, number: int) -> ToDoList:
        to_do_list = self.get_list(user)
        if number < len(to_do_list.items):
            del to_do_list.items[number]
        self.repository.write(user.login, to_do_list)
        return to_do_list

    def __create_list(self, user: User) -> ToDoList:
        to_do_list = ToDoList([])
        self.repository.write(user.login, to_do_list)
        return to_do_list


to_do_list_service = ToDoListService(to_do_list_repository)
