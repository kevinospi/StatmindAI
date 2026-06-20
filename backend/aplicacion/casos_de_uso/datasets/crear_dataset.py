from infraestructura.base_de_datos.modelos.dataset_modelo import DatasetModelo
from infraestructura.base_de_datos.repositorios.repositorio_dataset import RepositorioDataset
from aplicacion.validadores.validador_dataset import ValidadorDataset


class CrearDataset:
    def __init__(
        self,
        repositorio_dataset: RepositorioDataset,
        validador_dataset: ValidadorDataset,
    ) -> None:
        self._repositorio_dataset = repositorio_dataset
        self._validador_dataset = validador_dataset

    def ejecutar(
        self,
        usuario_id: str,
        nombre_archivo: str,
        tipo_archivo: str,
        ruta_archivo: str,
        tamaño_archivo: int,
        numero_filas: int | None = None,
        numero_columnas: int | None = None,
        columnas: list | None = None,
        tipos_datos: dict | None = None,
    ) -> DatasetModelo:
        self._validador_dataset.validar(
            nombre_archivo=nombre_archivo,
            tamaño_bytes=tamaño_archivo,
        )

        nuevo_dataset = DatasetModelo(
            usuario_id=usuario_id,
            nombre_archivo=nombre_archivo,
            tipo_archivo=tipo_archivo,
            ruta_archivo=ruta_archivo,
            tamaño_archivo=tamaño_archivo,
            numero_filas=numero_filas,
            numero_columnas=numero_columnas,
            columnas=columnas,
            tipos_datos=tipos_datos,
        )

        self._repositorio_dataset.crear(nuevo_dataset)
        self._repositorio_dataset.guardar_cambios()
        return nuevo_dataset