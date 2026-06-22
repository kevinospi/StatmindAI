import pandas as pd


class FormatoArchivoNoSoportadoError(Exception):
    pass


class LectorDataset:
    def leer(self, ruta_archivo: str, tipo_archivo: str) -> pd.DataFrame:
        if tipo_archivo == "csv":
            return pd.read_csv(ruta_archivo)

        if tipo_archivo == "xlsx":
            return pd.read_excel(ruta_archivo)

        raise FormatoArchivoNoSoportadoError(
            f"Tipo de archivo '{tipo_archivo}' no soportado por el lector de datasets."
        )