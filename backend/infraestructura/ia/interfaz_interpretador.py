from abc import ABC, abstractmethod

from infraestructura.ia.dto_interpretacion import ResultadoInterpretacion


class InterpretadorInforme(ABC):
    @abstractmethod
    def interpretar(
        self,
        estadisticas_descriptivas: dict | None,
        analisis_distribucion: dict | None,
        correlaciones: dict | None,
        deteccion_outliers: dict | None,
    ) -> ResultadoInterpretacion:
        raise NotImplementedError