from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from jose import JWTError, jwt

from infraestructura.configuracion.settings import obtener_settings

TipoToken = Literal["access", "refresh"]


class TokenInvalidoError(Exception):
    pass


class GestorJWT:
    def __init__(self) -> None:
        self._settings = obtener_settings()

    def crear_access_token(self, usuario_id: str) -> str:
        expiracion = datetime.now(timezone.utc) + timedelta(
            minutes=self._settings.jwt_access_token_expire_minutes
        )
        return self._codificar(usuario_id, "access", expiracion)

    def crear_refresh_token(self, usuario_id: str) -> str:
        expiracion = datetime.now(timezone.utc) + timedelta(
            days=self._settings.jwt_refresh_token_expire_days
        )
        return self._codificar(usuario_id, "refresh", expiracion)

    def decodificar(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self._settings.jwt_secret_key,
                algorithms=[self._settings.jwt_algorithm],
            )
        except JWTError as error:
            raise TokenInvalidoError("El token proporcionado es inválido o ha expirado.") from error

    def extraer_usuario_id(self, token: str, tipo_esperado: TipoToken) -> str:
        payload = self.decodificar(token)

        if payload.get("tipo") != tipo_esperado:
            raise TokenInvalidoError(
                f"Se esperaba un token de tipo '{tipo_esperado}', recibido '{payload.get('tipo')}'."
            )

        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise TokenInvalidoError("El token no contiene un identificador de usuario válido.")

        return usuario_id

    def _codificar(self, usuario_id: str, tipo: TipoToken, expiracion: datetime) -> str:
        payload: dict[str, Any] = {
            "sub": usuario_id,
            "tipo": tipo,
            "exp": expiracion,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, self._settings.jwt_secret_key, algorithm=self._settings.jwt_algorithm)