from ninja import Schema
from pydantic import EmailStr

class RegisterSchema(Schema):
    username: str
    email: EmailStr # Verificação do Pydantic se o email é valido
    password: str

class UserOut(Schema):
    id: int
    username: str
    email: str

class EmailLoginSchema(Schema):
    email: str
    password: str