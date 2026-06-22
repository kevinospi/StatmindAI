from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from aplicacion.excepciones import AccesoDenegadoError, InformeNoEncontradoError


class ObtenerInforme:
    def __init__(self, repositorio_informe: RepositorioInforme) -> None:
        self._repositorio_informe = repositorio_informe

    def ejecutar(self, informe_id: str, usuario_id: str) -> InformeModelo:
        informe = self._repositorio_informe.obtener_por_id(informe_id)
        if informe is None:
            raise InformeNoEncontradoError(f"No existe un informe con id '{informe_id}'.")

        if informe.usuario_id != usuario_id:
            raise AccesoDenegadoError("No tienes permiso para acceder a este informe.")

        return informe