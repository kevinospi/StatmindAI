from abc import ABC, abstractmethod

from infraestructura.ia.dto_conversacion import ContextoInforme, RespuestaConversacional


class InterpretadorConversacional(ABC):
    @abstractmethod
    def responder(
        self,
        contexto: ContextoInforme,
        mensaje_usuario: str,
    ) -> RespuestaConversacional:
        raise NotImplementedError