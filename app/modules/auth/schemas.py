from pydantic import BaseModel

TOKEN_TYPE_BEARER = "bearer"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = TOKEN_TYPE_BEARER
