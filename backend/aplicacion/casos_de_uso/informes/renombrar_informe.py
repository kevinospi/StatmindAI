from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from aplicacion.excepciones import (
    AccesoDenegadoError,
    InformeNoEncontradoError,
    TituloInvalidoError,
)


class RenombrarInforme:
    def __init__(self, repositorio_informe: RepositorioInforme) -> None:
        self._repositorio_informe = repositorio_informe

    def ejecutar(
        self,
        informe_id: str,
        usuario_id: str,
        nuevo_titulo: str,
    ) -> InformeModelo:
        informe = self._repositorio_informe.obtener_por_id(informe_id)
        if informe is None:
            raise InformeNoEncontradoError(f"No existe un informe con id '{informe_id}'.")

        if informe.usuario_id != usuario_id:
            raise AccesoDenegadoError("No tienes permiso para renombrar este informe.")

        titulo_limpio = nuevo_titulo.strip()
        if not (3 <= len(titulo_limpio) <= 150):
            raise TituloInvalidoError(
                "El título debe tener entre 3 y 150 caracteres."
            )

        informe.titulo = titulo_limpio
        self._repositorio_informe.actualizar(informe)
        self._repositorio_informe.guardar_cambios()
        return informe