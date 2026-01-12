from django.contrib.auth.models import User
from django.db import IntegrityError

class UserService:
    # Createuser do django já realiza automaticamente o hash da senha(PBKDF2 + SHA256)
    @staticmethod
    def create_user(*, username: str, email: str, password: str) -> User:
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            return user
        except IntegrityError:
            raise ValueError("Usuário já existe")