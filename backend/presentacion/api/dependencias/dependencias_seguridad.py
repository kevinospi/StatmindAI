from infraestructura.seguridad.gestor_password import GestorPassword
from infraestructura.seguridad.gestor_jwt import GestorJWT


def obtener_gestor_password() -> GestorPassword:
    return GestorPassword()


def obtener_gestor_jwt() -> GestorJWT:
    return GestorJWT()