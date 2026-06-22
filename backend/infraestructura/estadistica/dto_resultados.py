from dataclasses import dataclass, field


@dataclass
class EstadisticasColumnaNumerica:
    columna: str
    media: float
    mediana: float
    desviacion_estandar: float
    minimo: float
    maximo: float


@dataclass
class ValoresNulos:
    por_columna: dict[str, int]
    total: int


@dataclass
class MetadatosDataset:
    numero_filas: int
    numero_columnas: int
    nombres_columnas: list[str]
    tipos_datos: dict[str, str]


@dataclass
class ClasificacionVariables:
    numericas: list[str]
    categoricas: list[str]


@dataclass
class ResultadoMotorEstadistico:
    metadatos: MetadatosDataset
    valores_nulos: ValoresNulos
    clasificacion_variables: ClasificacionVariables
    estadisticas_descriptivas: list[EstadisticasColumnaNumerica] = field(default_factory=list)