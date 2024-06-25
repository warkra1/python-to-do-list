import hashlib
from app.models.user import User


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.md5(password.encode()).hexdigest()

    @classmethod
    def check_password(cls, user: User, password: str) -> bool:
        return user.password == cls.hash_password(password)
