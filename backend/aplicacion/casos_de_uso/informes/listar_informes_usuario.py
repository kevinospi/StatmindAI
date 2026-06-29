from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme


class ListarInformesUsuario:
    def __init__(self, repositorio_informe: RepositorioInforme) -> None:
        self._repositorio_informe = repositorio_informe

    def ejecutar(self, usuario_id: str) -> list[InformeModelo]:
        return self._repositorio_informe.listar_por_usuario_ordenado(usuario_id)