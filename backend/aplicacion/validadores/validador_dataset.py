from aplicacion.excepciones import (
    ArchivoVacioError,
    ExtensionNoSoportadaError,
    TamañoArchivoExcedidoError,
)

EXTENSIONES_SOPORTADAS = {"csv", "xlsx"}
TAMAÑO_MAXIMO_BYTES = 250 * 1024 * 1024


class ValidadorDataset:
    def validar(self, nombre_archivo: str, tamaño_bytes: int) -> None:
        extension = self._extraer_extension(nombre_archivo)

        if extension not in EXTENSIONES_SOPORTADAS:
            raise ExtensionNoSoportadaError(
                f"Extensión '.{extension}' no soportada. "
                f"Formatos permitidos: {', '.join(sorted(EXTENSIONES_SOPORTADAS))}."
            )

        if tamaño_bytes <= 0:
            raise ArchivoVacioError("El archivo está vacío.")

        if tamaño_bytes > TAMAÑO_MAXIMO_BYTES:
            raise TamañoArchivoExcedidoError(
                f"El archivo excede el tamaño máximo permitido de "
                f"{TAMAÑO_MAXIMO_BYTES // (1024 * 1024)} MB."
            )

    def _extraer_extension(self, nombre_archivo: str) -> str:
        if "." not in nombre_archivo:
            raise ExtensionNoSoportadaError(
                f"El archivo '{nombre_archivo}' no tiene extensión."
            )
        return nombre_archivo.rsplit(".", maxsplit=1)[-1].lower()