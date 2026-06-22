from infraestructura.ia.dto_interpretacion import ResultadoInterpretacion
from infraestructura.ia.interfaz_interpretador import InterpretadorInforme

UMBRAL_NULOS_ALTO_PORCENTAJE = 0.20
UMBRAL_ASIMETRIA_FUERTE = 1.0
UMBRAL_CURTOSIS_FUERTE = 3.0


class InterpretadorReglas(InterpretadorInforme):
    def interpretar(
        self,
        estadisticas_descriptivas: dict | None,
        analisis_distribucion: dict | None,
        correlaciones: dict | None,
        deteccion_outliers: dict | None,
    ) -> ResultadoInterpretacion:
        hallazgos = self._generar_hallazgos(
            estadisticas_descriptivas, analisis_distribucion, correlaciones, deteccion_outliers
        )
        recomendaciones = self._generar_recomendaciones(
            estadisticas_descriptivas, analisis_distribucion, correlaciones, deteccion_outliers
        )
        resumen_ejecutivo = self._generar_resumen_ejecutivo(estadisticas_descriptivas, hallazgos)
        conclusiones = self._generar_conclusiones(hallazgos, recomendaciones)

        return ResultadoInterpretacion(
            resumen_ejecutivo=resumen_ejecutivo,
            conclusiones=conclusiones,
            hallazgos_principales=hallazgos,
            recomendaciones=recomendaciones,
        )

    def _generar_hallazgos(
        self,
        estadisticas_descriptivas: dict | None,
        analisis_distribucion: dict | None,
        correlaciones: dict | None,
        deteccion_outliers: dict | None,
    ) -> dict:
        hallazgos: list[str] = []

        if estadisticas_descriptivas:
            hallazgos.extend(self._hallazgos_nulos(estadisticas_descriptivas))

        if correlaciones:
            hallazgos.extend(self._hallazgos_correlaciones(correlaciones))

        if deteccion_outliers:
            hallazgos.extend(self._hallazgos_outliers(deteccion_outliers))

        if analisis_distribucion:
            hallazgos.extend(self._hallazgos_distribucion(analisis_distribucion))

        if not hallazgos:
            hallazgos.append("No se detectaron patrones relevantes con las reglas actuales.")

        return {"items": hallazgos}

    def _hallazgos_nulos(self, estadisticas_descriptivas: dict) -> list[str]:
        items: list[str] = []
        metadatos = estadisticas_descriptivas.get("metadatos", {})
        valores_nulos = estadisticas_descriptivas.get("valores_nulos", {})

        numero_filas = metadatos.get("numero_filas", 0)
        por_columna = valores_nulos.get("por_columna", {})

        if numero_filas <= 0:
            return items

        for columna, cantidad in por_columna.items():
            porcentaje = cantidad / numero_filas
            if porcentaje >= UMBRAL_NULOS_ALTO_PORCENTAJE:
                items.append(
                    f"La columna '{columna}' tiene un {porcentaje:.0%} de valores nulos, "
                    f"un porcentaje considerable que podría afectar el análisis."
                )

        return items

    def _hallazgos_correlaciones(self, correlaciones: dict) -> list[str]:
        items: list[str] = []
        pares_relevantes = correlaciones.get("pares_relevantes", [])

        for par in pares_relevantes:
            columna_a = par.get("columna_a")
            columna_b = par.get("columna_b")
            coeficiente = par.get("coeficiente", 0)
            direccion = "positiva" if coeficiente > 0 else "negativa"
            items.append(
                f"Existe una correlación {direccion} fuerte entre '{columna_a}' y "
                f"'{columna_b}' (coeficiente: {coeficiente:.2f})."
            )

        return items

    def _hallazgos_outliers(self, deteccion_outliers: dict) -> list[str]:
        items: list[str] = []
        columnas = deteccion_outliers.get("columnas", [])

        for columna_info in columnas:
            cantidad = columna_info.get("cantidad_outliers", 0)
            if cantidad > 0:
                nombre_columna = columna_info.get("columna")
                items.append(
                    f"La columna '{nombre_columna}' presenta {cantidad} valor(es) atípico(s) "
                    f"detectado(s) mediante el método IQR."
                )

        return items

    def _hallazgos_distribucion(self, analisis_distribucion: dict) -> list[str]:
        items: list[str] = []
        columnas = analisis_distribucion.get("columnas", [])

        for columna_info in columnas:
            nombre_columna = columna_info.get("columna")
            asimetria = columna_info.get("asimetria", 0)
            curtosis = columna_info.get("curtosis", 0)

            if abs(asimetria) >= UMBRAL_ASIMETRIA_FUERTE:
                direccion = "hacia la derecha" if asimetria > 0 else "hacia la izquierda"
                items.append(
                    f"La variable '{nombre_columna}' muestra una asimetría marcada {direccion} "
                    f"(asimetría: {asimetria:.2f})."
                )

            if abs(curtosis) >= UMBRAL_CURTOSIS_FUERTE:
                items.append(
                    f"La variable '{nombre_columna}' tiene una curtosis elevada "
                    f"(curtosis: {curtosis:.2f}), lo que sugiere colas pesadas o un pico pronunciado."
                )

        return items

    def _generar_recomendaciones(
        self,
        estadisticas_descriptivas: dict | None,
        analisis_distribucion: dict | None,
        correlaciones: dict | None,
        deteccion_outliers: dict | None,
    ) -> dict:
        items: list[str] = []

        if estadisticas_descriptivas:
            valores_nulos = estadisticas_descriptivas.get("valores_nulos", {})
            if valores_nulos.get("total", 0) > 0:
                items.append(
                    "Considera evaluar estrategias de imputación o eliminación para los valores "
                    "nulos detectados antes de continuar con análisis más avanzados."
                )

        if deteccion_outliers:
            columnas = deteccion_outliers.get("columnas", [])
            if any(c.get("cantidad_outliers", 0) > 0 for c in columnas):
                items.append(
                    "Revisa los valores atípicos identificados para determinar si corresponden "
                    "a errores de captura o a variabilidad real de los datos."
                )

        if correlaciones:
            if correlaciones.get("pares_relevantes"):
                items.append(
                    "Las correlaciones fuertes detectadas podrían explorarse con modelos de "
                    "regresión u otras técnicas que aprovechen esa relación entre variables."
                )

        if not items:
            items.append(
                "No se identificaron alertas relevantes; el dataset puede analizarse con "
                "técnicas estándar sin tratamientos previos adicionales."
            )

        return {"items": items}

    def _generar_resumen_ejecutivo(
        self,
        estadisticas_descriptivas: dict | None,
        hallazgos: dict,
    ) -> str:
        if not estadisticas_descriptivas:
            return "No fue posible generar un resumen ejecutivo: no hay estadísticas disponibles."

        metadatos = estadisticas_descriptivas.get("metadatos", {})
        numero_filas = metadatos.get("numero_filas", 0)
        numero_columnas = metadatos.get("numero_columnas", 0)
        cantidad_hallazgos = len(hallazgos.get("items", []))

        return (
            f"El dataset analizado contiene {numero_filas} filas y {numero_columnas} columnas. "
            f"Se identificaron {cantidad_hallazgos} hallazgo(s) relevante(s) a partir de los "
            f"valores nulos, correlaciones, outliers y distribuciones calculadas."
        )

    def _generar_conclusiones(self, hallazgos: dict, recomendaciones: dict) -> str:
        cantidad_hallazgos = len(hallazgos.get("items", []))
        cantidad_recomendaciones = len(recomendaciones.get("items", []))

        return (
            f"A partir del análisis estadístico se generaron {cantidad_hallazgos} hallazgo(s) "
            f"y {cantidad_recomendaciones} recomendación(es). Estos resultados son producto de "
            f"reglas deterministas y no constituyen una interpretación generada por IA conversacional."
        )