from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from infraestructura.seguridad.gestor_jwt import GestorJWT, TokenInvalidoError

_esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def obtener_usuario_actual_id(token: str = Depends(_esquema_oauth2)) -> str:
    gestor_jwt = GestorJWT()
    try:
        return gestor_jwt.extraer_usuario_id(token, tipo_esperado="access")
    except TokenInvalidoError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error