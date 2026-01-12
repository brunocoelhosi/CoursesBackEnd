from ninja import Router
from .schemas import RegisterSchema, UserOut
from services.user_service import UserService
from django.contrib.auth.models import User
from ninja_jwt.authentication import JWTAuth

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja_jwt.tokens import RefreshToken
from .schemas import EmailLoginSchema
from ninja_jwt.authentication import JWTAuth

from ninja import Router
from typing import List
from courses.schemas import CourseOut, CourseIn, CourseUpdate
from services.course_service import CourseService
from ninja_jwt.authentication import JWTAuth

router = Router(tags=["Auth"])

@router.post("/register",
            response=UserOut,
            auth=None,
            summary="Cadastra um usuário",
            description=
            """
            Cadastra um usuário

                Parâmetros:

                    - username: INome do usuário
                    - email: Email do usuário
                    - password: Senha do usuário

                Retorna:

                    200 - Os dados de um curso.

                Erro: 
                    

            """,)
def register(request, payload: RegisterSchema):
    user = UserService.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
    )
    return user

@router.get("/me", response=UserOut, auth=JWTAuth())
def me(request):
    user: User = request.user
    return user

@router.post("/login",auth=None)
def login_with_email(request, payload: EmailLoginSchema):
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        return {"error": "Credenciais inválidas"}

    user = authenticate(
        username=user.username,
        password=payload.password
    )

    if not user:
        return {"error": "Credenciais inválidas"}

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }