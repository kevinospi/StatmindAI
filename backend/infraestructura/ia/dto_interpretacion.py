from dataclasses import dataclass, field


@dataclass
class ResultadoInterpretacion:
    resumen_ejecutivo: str
    conclusiones: str
    hallazgos_principales: dict
    recomendaciones: dict