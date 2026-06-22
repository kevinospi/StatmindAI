from pydantic import BaseModel


class LoginEsquema(BaseModel):
    email: str
    password: str


class TokenRespuestaEsquema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshEsquema(BaseModel):
    refresh_token: str


class AccessTokenRespuestaEsquema(BaseModel):
    access_token: str
    token_type: str = "bearer"