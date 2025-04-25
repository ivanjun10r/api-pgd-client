from .. import namedtuples

GET_METHOD = "GET"
DELETE_METHOD = "DELETE"
POST_METHOD = "POST"
PUT_METHOD = "PUT"
TOKEN_ENDPOINT = namedtuples.Endpoint("token", "/token", (POST_METHOD,))
USERS_ENDPOINT = namedtuples.Endpoint("users", "/users", (GET_METHOD, PUT_METHOD))
USER_ENDPOINT = namedtuples.Endpoint("user", "/user/{email}", (GET_METHOD, PUT_METHOD))
PLANO_ENTREGAS_ENDPOINT = namedtuples.Endpoint(
    "plano_entregas",
    "/organizacao/{origem_unidade}/{cod_unidade_autorizadora}/plano_entregas/{id_plano_entregas}",
    (GET_METHOD, PUT_METHOD),
)
PLANO_TRABALHO_ENDPOINT = namedtuples.Endpoint(
    "plano_trabalho",
    "/organizacao/{origem_unidade}/{cod_unidade_autorizadora}/plano_trabalho/{id_plano_trabalho}",
    (GET_METHOD, PUT_METHOD),
)
PARTICIPANTE_ENDPOINT = namedtuples.Endpoint(
    "participante",
    "/organizacao/{origem_unidade}/{cod_unidade_autorizadora}/{cod_unidade_lotacao}/participante/{matricula_siape}",
    (GET_METHOD, PUT_METHOD),
)
_ENDPOINTS = [
    TOKEN_ENDPOINT,
    USERS_ENDPOINT,
    USER_ENDPOINT,
    PLANO_ENTREGAS_ENDPOINT,
    PLANO_TRABALHO_ENDPOINT,
    PARTICIPANTE_ENDPOINT,
]
ENDPOINTS: dict[str, namedtuples.Endpoint] = {
    endpoint.name: endpoint for endpoint in _ENDPOINTS
}
