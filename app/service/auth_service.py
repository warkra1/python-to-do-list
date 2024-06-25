from typing import Optional
from app.models.user import User
from app.repository.user_repository import UserRepository, user_repository
from app.repository.repository import RepositoryInterface
from app.repository.exceptions import ModelNotFoundException
from .exceptions import AuthException
from app.infrastructure.password_hasher import PasswordHasher


class AuthService:
    __user: Optional[User] = None

    def __init__(self, repository: RepositoryInterface[User]):
        self.repository = repository

    @property
    def current_user(self) -> Optional[User]:
        return self.__user

    def login(self, login: str, password: str):
        try:
            user = self.repository.read(login)
        except ModelNotFoundException:
            raise AuthException.user_not_found()

        if not PasswordHasher.check_password(user, password):
            raise AuthException.invalid_password()

        self.__user = user

    def register(self, login: str, password: str):
        if self.__exists(login):
            raise AuthException.user_already_exists()

        user = User(login, PasswordHasher.hash_password(password))
        self.repository.write(login, user)
        self.__user = user

    def __exists(self, login: str) -> bool:
        try:
            self.repository.read(login)
            return True
        except ModelNotFoundException:
            return False


auth_service = AuthService(user_repository)
