from openai import APIConnectionError, APITimeoutError, AuthenticationError, OpenAI

from infraestructura.configuracion.settings import obtener_settings
from aplicacion.excepciones import ErrorProveedorIA


class ClienteOpenAI:
    def __init__(self) -> None:
        self._settings = obtener_settings()
        self._cliente: OpenAI | None = None

    def _obtener_cliente(self) -> OpenAI:
        if not self._settings.openai_api_key:
            raise ErrorProveedorIA(
                "OPENAI_API_KEY no está configurada. No es posible usar el proveedor OpenAI."
            )

        if self._cliente is None:
            self._cliente = OpenAI(api_key=self._settings.openai_api_key)

        return self._cliente

    def completar_chat(self, mensajes: list[dict], temperatura: float = 0.3) -> str:
        cliente = self._obtener_cliente()

        try:
            respuesta = cliente.chat.completions.create(
                model=self._settings.openai_model,
                messages=mensajes,
                temperature=temperatura,
                timeout=30.0,
            )
        except AuthenticationError as error:
            raise ErrorProveedorIA(
                "La API key de OpenAI fue rechazada. Verifica su validez."
            ) from error
        except APITimeoutError as error:
            raise ErrorProveedorIA(
                "El proveedor de IA no respondió a tiempo (timeout)."
            ) from error
        except APIConnectionError as error:
            raise ErrorProveedorIA(
                "No fue posible conectarse al proveedor de IA."
            ) from error
        except Exception as error:
            raise ErrorProveedorIA(
                f"Error inesperado al comunicarse con el proveedor de IA: {error}"
            ) from error

        if not respuesta.choices:
            raise ErrorProveedorIA("El proveedor de IA devolvió una respuesta vacía.")

        contenido = respuesta.choices[0].message.content
        if not contenido:
            raise ErrorProveedorIA("El proveedor de IA devolvió contenido vacío.")

        return contenido