from services.base import BaseService, BaseDataManager
from schemas.auth import (
    CreateUserSchema,
    UserSchema,
    TokenSchema,
)
from const import (
    TOKEN_EXPIRE_MINUTES,
    AUTH_URL,
    SECRET_KEY,
    TOKEN_ALGORITHM,
    TOKEN_TYPE,
)
from models.auth import UserModel

from sqlalchemy import select

from passlib.context import CryptContext

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from fastapi import Depends, status, HTTPException

from datetime import (
    datetime,
    timedelta,
)

import jwt

from jwt.exceptions import InvalidTokenError

import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl=AUTH_URL, auto_error=False)
logger = logging.getLogger("uvicorn.error")


async def get_current_user(token: str = Depends(oauth2_schema)) -> UserSchema | None:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        username: str = payload.get("username")
        email: str = payload.get("email")
        expires_at: str = payload.get("exp")
        if username is None:
            raise credential_exception
        if is_expired(expires_at):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")
    except InvalidTokenError:
        raise credential_exception
    return UserSchema(username, email)


def is_expired(expires_at: str) -> bool:
    return datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") < datetime.utcnow()


class HashingUtils:
    """Hashing and verifying passwords."""

    @staticmethod
    def hash_password(password: str) -> str | None:
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class AuthService(BaseService, HashingUtils):
    def create_user(self, user: CreateUserSchema) -> None:
        user_model = UserModel(
            name=user.name,
            email=user.email,
            role=user.email,
            hashed_password=self.bcrypt(user.password),
        )
        AuthDataManager(self.session).add_user(user_model)

    def authenticate(
        self, entered_user_data: OAuth2PasswordRequestForm = Depends()
    ) -> TokenSchema | None:
        user = AuthDataManager(self.session).get_user(entered_user_data.username)
        logger.debug(
            "this is a debug message" + str(user) + "    " + str(entered_user_data)
        )
        if user.hashed_password is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
        else:
            if not self.verify(entered_user_data.password, user.hashed_password):
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
            else:
                access_token = self._create_token(user.name, user.email)
                return TokenSchema(access_token=access_token, token_type=TOKEN_TYPE)

    def _create_token(self, name: str, email: str) -> str:
        payload = {
            "name": name,
            "sub": email,
            "expires_at": self._expiration_time(),
        }
        """SECRET_KEY????? or must use config.secret_key"""
        return jwt.encode(payload, SECRET_KEY, algorithm=TOKEN_ALGORITHM)

    @staticmethod
    def _expiration_time() -> str:
        """Get token expiration time."""

        expires_at = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        return expires_at.strftime("%Y-%m-%d %H:%M:%S")


class AuthDataManager(BaseDataManager):
    def add_user(self, user: UserModel) -> None:
        self.add_one(user)

    def get_user(self, name: str) -> UserSchema:
        model = self.get_one(select(UserModel).where(UserModel.name == name))
        if not isinstance(model, UserModel):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return UserSchema(
            name=model.name,
            email=model.email,
            hashed_password=model.hashed_password,
        )
