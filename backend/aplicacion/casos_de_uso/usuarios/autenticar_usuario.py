from infraestructura.base_de_datos.modelos.usuario_modelo import UsuarioModelo
from infraestructura.base_de_datos.repositorios.repositorio_usuario import RepositorioUsuario
from infraestructura.seguridad.gestor_password import GestorPassword
from aplicacion.excepciones import CredencialesInvalidasError


class AutenticarUsuario:
    def __init__(
        self,
        repositorio_usuario: RepositorioUsuario,
        gestor_password: GestorPassword,
    ) -> None:
        self._repositorio_usuario = repositorio_usuario
        self._gestor_password = gestor_password

    def ejecutar(self, email: str, password: str) -> UsuarioModelo:
        usuario = self._repositorio_usuario.obtener_por_email(email)

        if usuario is None or usuario.password_hash is None:
            raise CredencialesInvalidasError("Email o contraseña incorrectos.")

        if not self._gestor_password.verificar(password, usuario.password_hash):
            raise CredencialesInvalidasError("Email o contraseña incorrectos.")

        return usuario