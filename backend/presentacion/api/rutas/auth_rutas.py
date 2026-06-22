from fastapi import APIRouter, Depends

from aplicacion.casos_de_uso.usuarios.autenticar_usuario import AutenticarUsuario
from infraestructura.base_de_datos.repositorios.repositorio_usuario import RepositorioUsuario
from infraestructura.seguridad.gestor_jwt import GestorJWT, TokenInvalidoError
from infraestructura.seguridad.gestor_password import GestorPassword
from presentacion.api.dependencias.dependencias_db import obtener_repositorio_usuario
from presentacion.api.dependencias.dependencias_seguridad import (
    obtener_gestor_jwt,
    obtener_gestor_password,
)
from presentacion.esquemas.auth.auth_esquema import (
    AccessTokenRespuestaEsquema,
    LoginEsquema,
    RefreshEsquema,
    TokenRespuestaEsquema,
)
from aplicacion.excepciones import CredencialesInvalidasError
from fastapi import HTTPException

router = APIRouter()


@router.post("/auth/login", response_model=TokenRespuestaEsquema, tags=["Auth"])
def login(
    datos: LoginEsquema,
    repositorio_usuario: RepositorioUsuario = Depends(obtener_repositorio_usuario),
    gestor_password: GestorPassword = Depends(obtener_gestor_password),
    gestor_jwt: GestorJWT = Depends(obtener_gestor_jwt),
) -> TokenRespuestaEsquema:
    caso_de_uso = AutenticarUsuario(repositorio_usuario, gestor_password)

    try:
        usuario = caso_de_uso.ejecutar(email=datos.email, password=datos.password)
    except CredencialesInvalidasError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error

    access_token = gestor_jwt.crear_access_token(usuario.id)
    refresh_token = gestor_jwt.crear_refresh_token(usuario.id)

    return TokenRespuestaEsquema(access_token=access_token, refresh_token=refresh_token)


@router.post("/auth/refresh", response_model=AccessTokenRespuestaEsquema, tags=["Auth"])
def refrescar_token(
    datos: RefreshEsquema,
    gestor_jwt: GestorJWT = Depends(obtener_gestor_jwt),
) -> AccessTokenRespuestaEsquema:
    try:
        usuario_id = gestor_jwt.extraer_usuario_id(datos.refresh_token, tipo_esperado="refresh")
    except TokenInvalidoError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error

    nuevo_access_token = gestor_jwt.crear_access_token(usuario_id)

    return AccessTokenRespuestaEsquema(access_token=nuevo_access_token)