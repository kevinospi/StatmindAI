import numpy as np
import pandas as pd

from infraestructura.estadistica.dto_resultados import (
    ClasificacionVariables,
    EstadisticasColumnaNumerica,
    MetadatosDataset,
    ResultadoMotorEstadistico,
    ValoresNulos,
)
from infraestructura.estadistica.lector_dataset import LectorDataset


class MotorEstadistico:
    def __init__(self, lector_dataset: LectorDataset | None = None) -> None:
        self._lector_dataset = lector_dataset or LectorDataset()

    def analizar(self, ruta_archivo: str, tipo_archivo: str) -> ResultadoMotorEstadistico:
        dataframe = self._lector_dataset.leer(ruta_archivo, tipo_archivo)
        return self.analizar_dataframe(dataframe)

    def analizar_dataframe(self, dataframe: pd.DataFrame) -> ResultadoMotorEstadistico:
        metadatos = self._calcular_metadatos(dataframe)
        valores_nulos = self._calcular_valores_nulos(dataframe)
        clasificacion = self._clasificar_variables(dataframe)
        estadisticas = self._calcular_estadisticas_descriptivas(dataframe, clasificacion.numericas)

        return ResultadoMotorEstadistico(
            metadatos=metadatos,
            valores_nulos=valores_nulos,
            clasificacion_variables=clasificacion,
            estadisticas_descriptivas=estadisticas,
        )

    def _calcular_metadatos(self, dataframe: pd.DataFrame) -> MetadatosDataset:
        return MetadatosDataset(
            numero_filas=int(dataframe.shape[0]),
            numero_columnas=int(dataframe.shape[1]),
            nombres_columnas=list(dataframe.columns.astype(str)),
            tipos_datos={
                str(columna): str(dtype) for columna, dtype in dataframe.dtypes.items()
            },
        )

    def _calcular_valores_nulos(self, dataframe: pd.DataFrame) -> ValoresNulos:
        nulos_por_columna = dataframe.isnull().sum()
        return ValoresNulos(
            por_columna={
                str(columna): int(cantidad) for columna, cantidad in nulos_por_columna.items()
            },
            total=int(nulos_por_columna.sum()),
        )

    def _clasificar_variables(self, dataframe: pd.DataFrame) -> ClasificacionVariables:
        numericas = list(dataframe.select_dtypes(include=[np.number]).columns.astype(str))
        categoricas = [
            str(columna) for columna in dataframe.columns if str(columna) not in numericas
        ]
        return ClasificacionVariables(numericas=numericas, categoricas=categoricas)

    def _calcular_estadisticas_descriptivas(
        self,
        dataframe: pd.DataFrame,
        columnas_numericas: list[str],
    ) -> list[EstadisticasColumnaNumerica]:
        resultados: list[EstadisticasColumnaNumerica] = []

        for columna in columnas_numericas:
            serie = dataframe[columna].dropna()

            if serie.empty:
                continue

            resultados.append(
                EstadisticasColumnaNumerica(
                    columna=columna,
                    media=float(serie.mean()),
                    mediana=float(serie.median()),
                    desviacion_estandar=float(serie.std()) if len(serie) > 1 else 0.0,
                    minimo=float(serie.min()),
                    maximo=float(serie.max()),
                )
            )

        return resultados