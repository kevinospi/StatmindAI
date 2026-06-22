from infraestructura.ia.dto_conversacion import ContextoInforme, RespuestaConversacional
from infraestructura.ia.interfaz_interpretador_conversacional import InterpretadorConversacional


class InterpretadorConversacionalReglas(InterpretadorConversacional):
    def responder(
        self,
        contexto: ContextoInforme,
        mensaje_usuario: str,
    ) -> RespuestaConversacional:
        mensaje_normalizado = mensaje_usuario.strip().lower()

        if not contexto.resumen_ejecutivo and not contexto.conclusiones:
            return RespuestaConversacional(
                contenido=(
                    "Este informe todavía no ha sido interpretado. "
                    "Primero debes generar su interpretación antes de poder conversar sobre él."
                )
            )

        if "resumen" in mensaje_normalizado or "resumen ejecutivo" in mensaje_normalizado:
            return RespuestaConversacional(contenido=contexto.resumen_ejecutivo or "No hay resumen ejecutivo disponible.")

        if "conclusion" in mensaje_normalizado:
            return RespuestaConversacional(contenido=contexto.conclusiones or "No hay conclusiones disponibles.")

        if "hallazgo" in mensaje_normalizado:
            return RespuestaConversacional(contenido=self._formatear_lista(contexto.hallazgos_principales))

        if "recomendacion" in mensaje_normalizado:
            return RespuestaConversacional(contenido=self._formatear_lista(contexto.recomendaciones))

        return RespuestaConversacional(
            contenido=(
                "Puedo contarte sobre el resumen ejecutivo, las conclusiones, los hallazgos "
                "principales o las recomendaciones de este informe. "
                "¿Sobre cuál de estos te gustaría conversar?"
            )
        )

    def _formatear_lista(self, datos: dict | None) -> str:
        if not datos or not datos.get("items"):
            return "No hay elementos disponibles en esta sección."

        items = datos["items"]
        return "\n".join(f"- {item}" for item in items)