class AuthException(Exception):
    @classmethod
    def user_not_found(cls):
        return cls("User not found")

    @classmethod
    def invalid_password(cls):
        return cls("Invalid password")

    @classmethod
    def user_already_exists(cls):
        return cls("User already exists")


class ToDoListException(Exception):
    @classmethod
    def invalid_number(cls):
        return cls("Invalid item number")
