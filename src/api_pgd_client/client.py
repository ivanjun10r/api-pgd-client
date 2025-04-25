import abc
import json
from collections.abc import Callable
from typing import Any

import requests  # type: ignore

from . import constants, entities, namedtuples
from .constants import endpoints, errors, headers
from .utils import headers as headers_utils


class BaseRequest(abc.ABC):
    def do_delete(self, url: str, headers: dict[str, str]) -> Any:
        return self._do_request(endpoints.DELETE_METHOD, url, headers=headers)

    def do_get(self, url: str, params: dict[str, Any], headers: dict[str, str]) -> Any:
        return self._do_request(
            endpoints.GET_METHOD, url, params=params, headers=headers
        )

    def do_post(
        self,
        url: str,
        data: dict[str, Any],
        headers: dict[str, str],
        as_json: bool = True,
    ) -> Any:
        if as_json:
            data = json.dumps(data)  # type: ignore
        return self._do_request(endpoints.POST_METHOD, url, data=data, headers=headers)

    def do_put(self, url: str, data: dict[str, Any], headers: dict[str, str]) -> Any:
        payload = json.loads(json.dumps(data, default=str))
        return self._do_request(
            endpoints.PUT_METHOD, url, json=payload, headers=headers
        )

    def _do_request(self, method_name: str, url: str, **kwargs: Any) -> Any:
        kwargs.setdefault("timeout", constants.REQUEST_TIMEOUT)
        try:
            response = getattr(requests, method_name.lower())(url, **kwargs)
        except requests.Timeout as exc:
            error_class = self.get_error_class()
            raise error_class(
                f"Due to timeout error, {method_name.upper()} can't be done."
            ) from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            content = json.dumps(response.json(), ensure_ascii=False, indent=4)
            raise self.get_error_class()(
                f"Error while trying to do a {method_name.upper()} request.\n"
                f"Status code: {response.status_code}\n"
                f"Response:\n{content}"
            ) from exc
        return json.loads(response.content) if response.content else None

    @abc.abstractmethod
    def get_error_class(self) -> Any:
        pass


class ApiClient(BaseRequest):
    class Error(Exception):
        pass

    def __init__(
        self,
        domain: str = constants.BASE_URL,
        origem_unidade: Any = None,
        cod_unidade_autorizadora: Any = None,
    ):
        self.domain = domain
        self.origem_unidade = origem_unidade
        self.cod_unidade_autorizadora = cod_unidade_autorizadora
        self._token: dict[str, str] = {}

    @property
    def default_headers(self) -> dict[str, str]:
        return headers_utils.create_headers_with(
            [
                headers.CONTENT_TYPE_JSON_HEADER,
                headers_utils.authorization_header_factory(**self.token),
                headers_utils.header_item_factory(
                    headers.USER_AGENT_HEADER,
                    system_name=constants.SOURCE_SYSTEM_NAME,
                    system_version=constants.SOURCE_SYSTEM_VERSION,
                    system_url=constants.SOURCE_SYSTEM_ABOUT_URL,
                ),
            ],
        )

    @property
    def token(self) -> dict[str, str]:
        if not self._token:
            self._token = self.get_token()
        return self._token

    def get_token(self) -> Any:
        payload = {
            "username": constants.API_USERNAME,
            "password": constants.API_PASSWORD,
        }
        return self.do_post(
            self.token_endpoint,
            payload,
            headers_utils.create_headers_with(
                [headers.CONTENT_TYPE_FORM_URLENCODED_HEADER]
            ),
            as_json=False,
        )

    @property
    def token_endpoint(self) -> str:
        return self.get_endpoint(endpoints.TOKEN_ENDPOINT)

    def get_endpoint(self, endpoint: namedtuples.Endpoint, **kwargs: Any) -> str:
        base_path = self._get_endpoint_path(endpoint)
        try:
            path = base_path.format(**kwargs)
        except KeyError as exc:
            raise self.get_error_class()("Endpoint malformed") from exc
        return f"{self.domain}{path}"

    def _get_endpoint_path(self, endpoint: namedtuples.Endpoint) -> Any:
        try:
            return endpoints.ENDPOINTS[endpoint.name].path
        except (AttributeError, KeyError) as exc:
            error_class = self.get_error_class()
            raise error_class("Endpoint not defined") from exc

    def get_error_class(self) -> Any:
        return self.Error

    @property
    def users_endpoint(self) -> str:
        return self.get_endpoint(endpoints.USERS_ENDPOINT)

    def user_endpoint(self, email: str) -> str:
        return self.get_endpoint(endpoints.USER_ENDPOINT, email=email)

    def plano_entregas_endpoint(
        self,
        id_plano_entregas: str,
        origem_unidade: str = "",
        cod_unidade_autorizadora: int = 0,
    ) -> str:
        if not origem_unidade:
            origem_unidade = self.origem_unidade
        if not cod_unidade_autorizadora:
            cod_unidade_autorizadora = self.cod_unidade_autorizadora
        return self.get_endpoint(
            endpoints.PLANO_ENTREGAS_ENDPOINT,
            origem_unidade=origem_unidade,
            cod_unidade_autorizadora=cod_unidade_autorizadora,
            id_plano_entregas=id_plano_entregas,
        )

    def plano_trabalho_endpoint(
        self,
        id_plano_trabalho: str,
        origem_unidade: str = "",
        cod_unidade_autorizadora: int = 0,
    ) -> str:
        if not origem_unidade:
            origem_unidade = self.origem_unidade
        if not cod_unidade_autorizadora:
            cod_unidade_autorizadora = self.cod_unidade_autorizadora
        return self.get_endpoint(
            endpoints.PLANO_TRABALHO_ENDPOINT,
            origem_unidade=origem_unidade,
            cod_unidade_autorizadora=cod_unidade_autorizadora,
            id_plano_trabalho=id_plano_trabalho,
        )

    def participante_endpoint(
        self,
        cod_unidade_lotacao: int,
        matricula_siape: str,
        origem_unidade: str = "",
        cod_unidade_autorizadora: int = 0,
    ) -> str:
        if not origem_unidade:
            origem_unidade = self.origem_unidade
        if not cod_unidade_autorizadora:
            cod_unidade_autorizadora = self.cod_unidade_autorizadora
        return self.get_endpoint(
            endpoints.PARTICIPANTE_ENDPOINT,
            origem_unidade=origem_unidade,
            cod_unidade_autorizadora=cod_unidade_autorizadora,
            cod_unidade_lotacao=cod_unidade_lotacao,
            matricula_siape=matricula_siape,
        )

    def consultar_usuario(self, email: str) -> entities.User:
        response = self.retry_on_expired_token(
            lambda: self.do_get(self.user_endpoint(email), {}, self.default_headers)
        )
        return entities.User(**response)

    def consultar_participante(
        self,
        cod_unidade_lotacao: int,
        matricula_siape: str,
        origem_unidade: str = "",
        cod_unidade_autorizadora: int = 0,
    ) -> entities.Participante:
        response = self.retry_on_expired_token(
            self.do_get,
            self.participante_endpoint(
                cod_unidade_lotacao,
                matricula_siape,
                origem_unidade,
                cod_unidade_autorizadora,
            ),
            {},
            self.default_headers,
        )
        return entities.Participante(**response)

    def enviar_participante(self, participante: entities.Participante) -> Any:
        return self.retry_on_expired_token(
            self.do_put,
            self.participante_endpoint(
                participante.cod_unidade_lotacao,
                participante.matricula_siape,
                participante.origem_unidade,
                participante.cod_unidade_autorizadora,
            ),
            participante.to_dict(),
            self.default_headers,
        )

    def consultar_plano_entregas(
        self,
        id_plano_entregas: str,
        origem_unidade: str = "",
        cod_unidade_autorizadora: int = 0,
    ) -> entities.PlanoDeEntregas:
        response = self.retry_on_expired_token(
            lambda: self.do_get(
                self.plano_entregas_endpoint(
                    id_plano_entregas, origem_unidade, cod_unidade_autorizadora
                ),
                {},
                self.default_headers,
            )
        )
        return entities.PlanoDeEntregas(**response)

    def enviar_plano_entregas(self, plano_entregas: entities.PlanoDeEntregas) -> Any:
        return self.retry_on_expired_token(
            self.do_put,
            self.plano_entregas_endpoint(
                plano_entregas.id_plano_entregas,
                plano_entregas.origem_unidade,
                plano_entregas.cod_unidade_autorizadora,
            ),
            plano_entregas.to_dict(),
            self.default_headers,
        )

    def consultar_plano_trabalho(
        self,
        id_plano_trabalho: str,
        origem_unidade: str = "",
        cod_unidade_autorizadora: int = 0,
    ) -> entities.PlanoDeTrabalho:
        response = self.retry_on_expired_token(
            self.do_get,
            self.plano_trabalho_endpoint(
                id_plano_trabalho, origem_unidade, cod_unidade_autorizadora
            ),
            {},
            self.default_headers,
        )
        return entities.PlanoDeTrabalho(**response)

    def enviar_plano_trabalho(self, plano_trabalho: entities.PlanoDeTrabalho) -> Any:
        return self.retry_on_expired_token(
            self.do_put,
            self.plano_trabalho_endpoint(
                plano_trabalho.id_plano_trabalho,
                plano_trabalho.origem_unidade,
                plano_trabalho.cod_unidade_autorizadora,
            ),
            plano_trabalho.to_dict(),
            self.default_headers,
        )

    def retry_on_expired_token(
        self, request_call: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        try:
            response = request_call(*args, **kwargs)
        except self.Error as exc:
            if errors.TOKEN_INVALIDO not in str(exc):
                raise exc
            self._token = self.get_token()
            response = request_call(*args, **kwargs)
        return response
