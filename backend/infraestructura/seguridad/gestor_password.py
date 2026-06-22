from passlib.context import CryptContext


class GestorPassword:
    def __init__(self) -> None:
        self._contexto = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hashear(self, password_plano: str) -> str:
        return self._contexto.hash(password_plano)

    def verificar(self, password_plano: str, password_hash: str) -> bool:
        return self._contexto.verify(password_plano, password_hash)