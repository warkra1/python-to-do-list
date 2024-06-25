from enum import Enum
from app.service.auth_service import AuthService
from app.service.to_do_list_service import ToDoListService
from .service.exceptions import AuthException
from .infrastructure.input_utils import ask_number
from .models.to_do_item import ToDoItem
from .service.auth_service import auth_service
from .service.to_do_list_service import to_do_list_service


class Commands(Enum):
    LOGIN = 'login'
    REGISTER = 'register'
    GET_LIST = 'get_list'
    CREATE_ITEM = 'create_item'
    UPDATE_ITEM = 'update_item'
    DELETE_ITEM = 'delete_item'
    EXIT = 'exit'
    HELP = 'help'

    @classmethod
    def try_from(cls, value):
        values = [item.value for item in cls]
        if value in values:
            return cls(value)
        return None


class CommandProcessor:
    def __init__(self, auth_service: AuthService, to_do_list_service: ToDoListService):
        self.auth_service = auth_service
        self.to_do_list_service = to_do_list_service

    def run(self):
        print("Hello, this is a to do list CLI App")

        while True:
            ans = input("Please, Enter a command (or type 'help' to see all commands): ")
            command = Commands.try_from(ans)

            if command == Commands.LOGIN:
                self.__login()
            elif command == Commands.REGISTER:
                self.__register()
            elif command == Commands.GET_LIST:
                self.__get_list()
            elif command == Commands.CREATE_ITEM:
                self.__create_item()
            elif command == Commands.UPDATE_ITEM:
                self.__update_item()
            elif command == Commands.DELETE_ITEM:
                self.__delete_item()
            elif command == Commands.HELP:
                self.__help()
            elif command == Commands.EXIT:
                self.__exit()
            else:
                print('Invalid command!')

    def __login(self):
        login = input('Enter login: ')
        password = input('Enter password: ')
        try:
            self.auth_service.login(login, password)
            print('Successfully logged in!')
        except AuthException as e:
            print(e.args[0])

    def __register(self):
        login = input('Enter login: ')
        password = input('Enter password: ')
        try:
            self.auth_service.register(login, password)
            print('Successfully registered!')
        except AuthException as e:
            print(e.args[0])

    def __get_list(self):
        if not self.__check_auth():
            return

        to_do_list = self.to_do_list_service.get_list(self.auth_service.current_user)
        print('To Do List:')
        if len(to_do_list.items) == 0:
            print("\tYour list is empty")
        else:
            for i, item in enumerate(to_do_list.items):
                print(f"\t[{i + 1}] {item.title}")

    def __create_item(self):
        if not self.__check_auth():
            return

        title = input('Enter title: ')
        number = ask_number('Enter number: ')

        self.to_do_list_service.create_item(
            self.auth_service.current_user,
            ToDoItem(title),
            number - 1
        )

        print('Item successfully created!')

    def __update_item(self):
        if not self.__check_auth():
            return

        number = ask_number('Enter a number of item: ')
        title = input('Enter title: ')

        self.to_do_list_service.update_item(
            self.auth_service.current_user,
            ToDoItem(title),
            number - 1
        )

        print("Item successfully updated!")

    def __delete_item(self):
        if not self.__check_auth():
            return

        number = ask_number('Enter a number of item: ')
        self.to_do_list_service.delete_item(self.auth_service.current_user, number - 1)
        print("Item successfully deleted!")

    def __help(self):
        print("List of commands:")
        print(f"\t{Commands.LOGIN.value} - authorize to application")
        print(f"\t{Commands.REGISTER.value} - create new user")
        print(f"\t{Commands.GET_LIST.value} - get current user's todo list")
        print(f"\t{Commands.CREATE_ITEM.value} - create a new item in todo list")
        print(f"\t{Commands.UPDATE_ITEM.value} - updates a specific item in list")
        print(f"\t{Commands.DELETE_ITEM.value} - deletes a specific item in list")
        print(f"\t{Commands.HELP.value} - show commands")
        print(f"\t{Commands.EXIT.value} - exit from application")

    def __exit(self):
        print('Bye!')
        exit()

    def __check_auth(self) -> bool:
        if self.auth_service.current_user is None:
            print("You should login first")
            return False
        return True


command_processor = CommandProcessor(auth_service, to_do_list_service)
