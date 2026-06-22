from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from infraestructura.ia.interfaz_interpretador import InterpretadorInforme
from aplicacion.excepciones import (
    AccesoDenegadoError,
    InformeNoEncontradoError,
    InformeSinAnalisisError,
)


class InterpretarInforme:
    def __init__(
        self,
        repositorio_informe: RepositorioInforme,
        interpretador_informe: InterpretadorInforme,
    ) -> None:
        self._repositorio_informe = repositorio_informe
        self._interpretador_informe = interpretador_informe

    def ejecutar(self, informe_id: str, usuario_id: str) -> InformeModelo:
        informe = self._repositorio_informe.obtener_por_id(informe_id)
        if informe is None:
            raise InformeNoEncontradoError(f"No existe un informe con id '{informe_id}'.")

        if informe.usuario_id != usuario_id:
            raise AccesoDenegadoError("No tienes permiso para interpretar este informe.")

        if informe.estadisticas_descriptivas is None:
            raise InformeSinAnalisisError(
                "El informe no tiene resultados estadísticos. "
                "Debes analizar el dataset antes de interpretarlo."
            )

        resultado = self._interpretador_informe.interpretar(
            estadisticas_descriptivas=informe.estadisticas_descriptivas,
            analisis_distribucion=informe.analisis_distribucion,
            correlaciones=informe.correlaciones,
            deteccion_outliers=informe.deteccion_outliers,
        )

        informe.resumen_ejecutivo = resultado.resumen_ejecutivo
        informe.conclusiones = resultado.conclusiones
        informe.hallazgos_principales = resultado.hallazgos_principales
        informe.recomendaciones = resultado.recomendaciones

        self._repositorio_informe.actualizar(informe)
        self._repositorio_informe.guardar_cambios()
        return informe