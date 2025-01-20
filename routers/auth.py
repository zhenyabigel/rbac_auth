from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.session import create_session
from rbac_auth.const import (
    AUTH_TAGS,
    AUTH_URL,
)
from schemas.auth import TokenSchema
from services.auth import AuthService


auth_router = APIRouter(prefix="/" + AUTH_URL, tags=AUTH_TAGS)


@auth_router.post("", response_model=TokenSchema)
async def auth(
    login: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(create_session),
) -> TokenSchema | None:
    return AuthService(session).authenticate(login)


