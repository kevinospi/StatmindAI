from infraestructura.base_de_datos.modelos.mensaje_modelo import MensajeModelo
from infraestructura.base_de_datos.repositorios.repositorio_conversacion import (
    RepositorioConversacion,
)
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme
from infraestructura.base_de_datos.repositorios.repositorio_mensaje import RepositorioMensaje
from infraestructura.ia.contexto_informe import ConstructorContextoInforme
from infraestructura.ia.interfaz_interpretador_conversacional import (
    InterpretadorConversacional,
)
from aplicacion.excepciones import (
    AccesoDenegadoError,
    ConversacionNoEncontradaError,
    ConversacionSinInformeError,
    InformeNoEncontradoError,
)


class ResponderMensajeInforme:
    def __init__(
        self,
        repositorio_conversacion: RepositorioConversacion,
        repositorio_mensaje: RepositorioMensaje,
        repositorio_informe: RepositorioInforme,
        interpretador_conversacional: InterpretadorConversacional,
        constructor_contexto: ConstructorContextoInforme | None = None,
    ) -> None:
        self._repositorio_conversacion = repositorio_conversacion
        self._repositorio_mensaje = repositorio_mensaje
        self._repositorio_informe = repositorio_informe
        self._interpretador_conversacional = interpretador_conversacional
        self._constructor_contexto = constructor_contexto or ConstructorContextoInforme()

    def ejecutar(
        self,
        conversacion_id: str,
        usuario_id: str,
        contenido_mensaje: str,
    ) -> MensajeModelo:
        conversacion = self._repositorio_conversacion.obtener_por_id(conversacion_id)
        if conversacion is None:
            raise ConversacionNoEncontradaError(
                f"No existe una conversación con id '{conversacion_id}'."
            )

        if conversacion.usuario_id != usuario_id:
            raise AccesoDenegadoError("No tienes permiso para conversar en esta conversación.")

        if conversacion.informe_id is None:
            raise ConversacionSinInformeError(
                "Esta conversación no está asociada a un informe."
            )

        informe = self._repositorio_informe.obtener_por_id(conversacion.informe_id)
        if informe is None:
            raise InformeNoEncontradoError(
                f"No existe un informe con id '{conversacion.informe_id}'."
            )

        historial_previo = self._repositorio_mensaje.obtener_por_conversacion(conversacion_id)

        mensaje_usuario = MensajeModelo(
            conversacion_id=conversacion_id,
            rol="usuario",
            contenido=contenido_mensaje,
        )
        self._repositorio_mensaje.crear(mensaje_usuario)
        self._repositorio_mensaje.guardar_cambios()

        contexto = self._constructor_contexto.construir(informe, historial_previo)
        respuesta = self._interpretador_conversacional.responder(contexto, contenido_mensaje)

        mensaje_asistente = MensajeModelo(
            conversacion_id=conversacion_id,
            rol="asistente",
            contenido=respuesta.contenido,
            tipo_respuesta=respuesta.tipo_respuesta,
        )
        self._repositorio_mensaje.crear(mensaje_asistente)
        self._repositorio_mensaje.guardar_cambios()

        return mensaje_asistente