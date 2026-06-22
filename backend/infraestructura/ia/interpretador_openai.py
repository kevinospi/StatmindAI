import json

from infraestructura.ia.cliente_openai import ClienteOpenAI
from infraestructura.ia.dto_interpretacion import ResultadoInterpretacion
from infraestructura.ia.interfaz_interpretador import InterpretadorInforme
from aplicacion.excepciones import ErrorProveedorIA

_PROMPT_SISTEMA = (
    "Eres un analista de datos senior que interpreta resultados estadísticos ya calculados. "
    "NUNCA realizas cálculos ni inventas cifras: tu única función es interpretar, en español, "
    "los números que se te proporcionan. No debes recalcular estadísticas, solo explicarlas. "
    "Responde EXCLUSIVAMENTE en formato JSON válido, sin texto adicional, con esta estructura exacta:\n"
    "{\n"
    '  "resumen_ejecutivo": "string",\n'
    '  "conclusiones": "string",\n'
    '  "hallazgos_principales": {"items": ["string", "string", ...]},\n'
    '  "recomendaciones": {"items": ["string", "string", ...]}\n'
    "}"
)


class InterpretadorOpenAI(InterpretadorInforme):
    def __init__(self, cliente_openai: ClienteOpenAI | None = None) -> None:
        self._cliente_openai = cliente_openai or ClienteOpenAI()

    def interpretar(
        self,
        estadisticas_descriptivas: dict | None,
        analisis_distribucion: dict | None,
        correlaciones: dict | None,
        deteccion_outliers: dict | None,
    ) -> ResultadoInterpretacion:
        prompt_usuario = self._construir_prompt_usuario(
            estadisticas_descriptivas, analisis_distribucion, correlaciones, deteccion_outliers
        )

        contenido_respuesta = self._cliente_openai.completar_chat(
            mensajes=[
                {"role": "system", "content": _PROMPT_SISTEMA},
                {"role": "user", "content": prompt_usuario},
            ]
        )

        return self._parsear_respuesta(contenido_respuesta)

    def _construir_prompt_usuario(
        self,
        estadisticas_descriptivas: dict | None,
        analisis_distribucion: dict | None,
        correlaciones: dict | None,
        deteccion_outliers: dict | None,
    ) -> str:
        return (
            "Interpreta los siguientes resultados estadísticos, ya calculados sobre un dataset. "
            "No inventes ni modifiques ningún número: úsalos exactamente como se presentan.\n\n"
            f"ESTADÍSTICAS DESCRIPTIVAS Y METADATOS:\n{json.dumps(estadisticas_descriptivas, ensure_ascii=False, indent=2)}\n\n"
            f"ANÁLISIS DE DISTRIBUCIÓN (asimetría y curtosis):\n{json.dumps(analisis_distribucion, ensure_ascii=False, indent=2)}\n\n"
            f"CORRELACIONES:\n{json.dumps(correlaciones, ensure_ascii=False, indent=2)}\n\n"
            f"DETECCIÓN DE OUTLIERS (método IQR):\n{json.dumps(deteccion_outliers, ensure_ascii=False, indent=2)}\n\n"
            "Genera:\n"
            "1. resumen_ejecutivo: una descripción general clara y profesional de los hallazgos.\n"
            "2. conclusiones: una síntesis final de lo que dicen los datos.\n"
            "3. hallazgos_principales: una lista de observaciones concretas basadas en los números anteriores.\n"
            "4. recomendaciones: una lista de sugerencias de análisis o acciones a partir de los datos.\n"
            "Responde únicamente con el JSON solicitado, sin explicaciones adicionales."
        )

    def _parsear_respuesta(self, contenido_respuesta: str) -> ResultadoInterpretacion:
        try:
            datos = json.loads(contenido_respuesta)
        except json.JSONDecodeError as error:
            raise ErrorProveedorIA(
                "El proveedor de IA devolvió una respuesta que no es JSON válido."
            ) from error

        campos_requeridos = {
            "resumen_ejecutivo",
            "conclusiones",
            "hallazgos_principales",
            "recomendaciones",
        }
        campos_faltantes = campos_requeridos - datos.keys()
        if campos_faltantes:
            raise ErrorProveedorIA(
                f"La respuesta del proveedor de IA no contiene los campos requeridos: "
                f"{', '.join(sorted(campos_faltantes))}."
            )

        return ResultadoInterpretacion(
            resumen_ejecutivo=datos["resumen_ejecutivo"],
            conclusiones=datos["conclusiones"],
            hallazgos_principales=datos["hallazgos_principales"],
            recomendaciones=datos["recomendaciones"],
        )