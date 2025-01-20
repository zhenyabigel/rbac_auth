from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    name: str
    email: str
    password: str
    role: str = "User"


class UserSchema(BaseModel):
    name: str
    email: str
    hashed_password: str | None

class TokenSchema(BaseModel):
    access_token: str
    token_type: str