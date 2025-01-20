from enum import Enum
from typing import Final, List

API_TITLE: Final = "Zheka API"
API_DESCRIPTION: Final = "SLlsd,sld,sld,sld,slmksfnsnfishifsjdosk"

AUTH_TAGS: Final[List[str | Enum] | None] = ["Authentication"]
AUTH_URL: Final = "token"

TOKEN_TYPE: Final = "bearer"
TOKEN_EXPIRE_MINUTES: Final = 60

TOKEN_ALGORITHM: Final = "HS256"

SECRET_KEY: Final = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

__version__ = "1.0.0"
