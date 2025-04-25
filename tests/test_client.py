import json
from collections import namedtuple
from unittest import TestCase, mock

import pytest
import requests

from api_pgd_client import client, constants, entities
from api_pgd_client.constants import endpoints as constants_endpoints
from api_pgd_client.constants import errors as constants_errors
from api_pgd_client.constants import headers as constants_headers


class MockResponse:
    def __init__(self, content=None, json_data=None, status_code=200, error=False):
        self._content = content if content else b"{}"
        self.json_data = json_data if json_data else json.loads(self._content)
        self.status_code = status_code
        self.ok = not error

    def json(self):
        return self.json_data

    @property
    def content(self):
        return self._content


class ConcreteRequest(client.BaseRequest):
    class Error(Exception):
        pass

    def get_error_class(self):
        return self.Error


class BaseRequestTestCase(TestCase):
    def setUp(self):
        self.request = ConcreteRequest()
        self.url = "http://example.com"
        self.headers = {"Authorization": "Bearer token"}
        self.data = {"key": "value"}

    @mock.patch("api_pgd_client.client.requests.get")
    def test_do_get_success(self, mock_get):
        mock_response = mock.MagicMock()
        mock_response.content = b'{"key": "value"}'
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response = self.request.do_get(self.url, {}, self.headers)

        self.assertEqual(response, {"key": "value"})
        mock_get.assert_called_once_with(
            self.url, params={}, headers=self.headers, timeout=constants.REQUEST_TIMEOUT
        )

    @mock.patch("api_pgd_client.client.requests.post")
    def test_do_post_success(self, mock_post):
        mock_response = mock.MagicMock()
        mock_response.content = b'{"key": "value"}'
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        response = self.request.do_post(self.url, self.data, self.headers)

        self.assertEqual(response, {"key": "value"})
        mock_post.assert_called_once_with(
            self.url,
            data='{"key": "value"}',
            headers=self.headers,
            timeout=constants.REQUEST_TIMEOUT,
        )

    @mock.patch("api_pgd_client.client.requests.put")
    def test_do_put_timeout_error(self, mock_put):
        mock_put.side_effect = requests.exceptions.Timeout()
        erro_esperado = "Due to timeout error, PUT can't be done."

        with self.assertRaises(self.request.Error) as context:
            self.request.do_put(self.url, self.data, self.headers)

        self.assertIn(erro_esperado, str(context.exception))
        payload = json.loads(json.dumps(self.data, default=str))
        mock_put.assert_called_once_with(
            self.url,
            json=payload,
            headers=self.headers,
            timeout=constants.REQUEST_TIMEOUT,
        )

    @mock.patch("api_pgd_client.client.requests.put")
    def test_do_get_http_error(self, mock_put):
        mock_response = MockResponse(content=b'{"detail": "value"}')
        mock_response.raise_for_status = mock.MagicMock(
            side_effect=requests.HTTPError("HTTP Error")
        )
        mock_put.return_value = mock_response
        erro_esperado = (
            "Error while trying to do a PUT request.\n"
            f"Status code: {mock_response.status_code}\n"
            f"Response:\n{json.dumps(mock_response.json(), ensure_ascii=False, indent=4)}"
        )

        with self.assertRaises(self.request.Error) as context:
            self.request.do_put(self.url, self.data, self.headers)

        self.assertIn(erro_esperado, str(context.exception))
        payload = json.loads(json.dumps(self.data, default=str))
        mock_put.assert_called_once_with(
            self.url,
            json=payload,
            headers=self.headers,
            timeout=constants.REQUEST_TIMEOUT,
        )

    @mock.patch("api_pgd_client.client.requests.put")
    def test_do_put_success(self, mock_put):
        mock_response = mock.MagicMock()
        mock_response.content = b'{"key": "value"}'
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response

        response = self.request.do_put(self.url, self.data, self.headers)

        self.assertEqual(response, {"key": "value"})
        mock_put.assert_called_once_with(
            self.url,
            json={"key": "value"},
            headers=self.headers,
            timeout=constants.REQUEST_TIMEOUT,
        )

    @mock.patch("api_pgd_client.client.requests.delete")
    def test_do_delete_success(self, mock_delete):
        mock_response = mock.MagicMock()
        mock_response.content = b'{"key": "value"}'
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response

        response = self.request.do_delete(self.url, self.headers)

        self.assertEqual(response, {"key": "value"})
        mock_delete.assert_called_once_with(
            self.url, headers=self.headers, timeout=constants.REQUEST_TIMEOUT
        )


class ApiClientTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.domain = "https://api-pgd.dth.api.gov.br"
        cls.origem_unidade = "SIAPE"
        cls.unidade_autorizadora = "999"
        cls.unidade_lotacao = "777"
        cls.matricula = "1234567"
        cls.email = "fulano@mail.com"
        cls.token = {"access_token": "token", "token_type": "Bearer"}

    def setUp(self):
        self.api_client = client.ApiClient(
            domain=self.domain,
            origem_unidade=self.origem_unidade,
            cod_unidade_autorizadora=self.unidade_autorizadora,
        )

    def tearDown(self):
        pass

    def test_default_headers_deveria_retornar_os_headers_padrao(self):
        expected_source = "my app/2025.3.1 (https://my.app.example/about)"
        self.api_client._token = self.token
        headers_esperados = {
            constants_headers.CONTENT_TYPE_HEADER_LABEL: constants_headers.CONTENT_TYPE_JSON_VALUE,
            constants_headers.AUTHORIZATION_HEADER_LABEL: constants_headers.AUTHORIZATION_HEADER.value.format(
                **self.token
            ),
            constants_headers.USER_AGENT_HEADER_LABEL: expected_source,
        }

        headers = self.api_client.default_headers
        assert headers_esperados == headers

    def test_get_endpoint_deveria_lancar_erro_quando_nao_definido(self):
        with pytest.raises(client.ApiClient.Error, match="Endpoint not defined"):
            self.api_client.get_endpoint("endpoint_inexistente")

    def test_get_endpoint_deveria_lancar_erro_estrutura_nao_possui_nome(self):
        SemNome = namedtuple("SemNome", ("name_", "path", "allowed_methods"))
        sem_nome_endpoint = SemNome("user", "/user/{email}", ("GET",))
        with pytest.raises(client.ApiClient.Error, match="Endpoint not defined"):
            self.api_client.get_endpoint(sem_nome_endpoint, email=self.email)

    def test_get_endpoint_deveria_lancar_erro_quando_mal_formado(self):
        with pytest.raises(client.ApiClient.Error, match="Endpoint malformed"):
            self.api_client.get_endpoint(
                constants_endpoints.USER_ENDPOINT, param_inexistente="fulano"
            )

    def test_get_endpoint_deveria_retornar_adequadamente_quando_parametros_definidos(
        self,
    ):
        endpoint_params = {"email": self.email}
        path = constants_endpoints.USER_ENDPOINT.path.format(**endpoint_params)
        url_esperada = f"{self.domain}{path}"
        assert url_esperada == self.api_client.get_endpoint(
            constants_endpoints.USER_ENDPOINT, **endpoint_params
        )

    def test_token_endpoint_deveria_estar_corretamente_definido(self):
        with mock.patch(
            "api_pgd_client.client.ApiClient.get_endpoint"
        ) as mock_get_endpoint:
            endpoint = self.api_client.token_endpoint
        assert endpoint == mock_get_endpoint.return_value
        mock_get_endpoint.assert_called_once_with(constants_endpoints.TOKEN_ENDPOINT)

    def test_users_endpoint_deveria_estar_corretamente_definido(self):
        api_client = client.ApiClient()
        with mock.patch(
            "api_pgd_client.client.ApiClient.get_endpoint"
        ) as mock_get_endpoint:
            endpoint = api_client.users_endpoint
        assert endpoint == mock_get_endpoint.return_value
        mock_get_endpoint.assert_called_once_with(constants_endpoints.USERS_ENDPOINT)

    def test_user_endpoint_deveria_estar_corretamente_definido(self):
        with mock.patch(
            "api_pgd_client.client.ApiClient.get_endpoint"
        ) as mock_get_endpoint:
            endpoint = self.api_client.user_endpoint(self.email)
        assert endpoint == mock_get_endpoint.return_value
        mock_get_endpoint.assert_called_once_with(
            constants_endpoints.USER_ENDPOINT, email=self.email
        )

    def test_plano_entregas_endpoint_deveria_estar_corretamente_definido(self):
        id_plano_entregas = 123
        with mock.patch(
            "api_pgd_client.client.ApiClient.get_endpoint"
        ) as mock_get_endpoint:
            endpoint = self.api_client.plano_entregas_endpoint(id_plano_entregas)
        assert endpoint == mock_get_endpoint.return_value
        mock_get_endpoint.assert_called_once_with(
            constants_endpoints.PLANO_ENTREGAS_ENDPOINT,
            origem_unidade=self.origem_unidade,
            cod_unidade_autorizadora=self.unidade_autorizadora,
            id_plano_entregas=id_plano_entregas,
        )

    def test_plano_entregas_endpoint_deveria_estar_corretamente_definido_com_valores_proprios(
        self,
    ):
        id_plano_entregas = 123
        api_client = client.ApiClient(
            origem_unidade="Nenhum", cod_unidade_autorizadora="000"
        )
        with mock.patch(
            "api_pgd_client.client.ApiClient.get_endpoint"
        ) as mock_get_endpoint:
            endpoint = api_client.plano_entregas_endpoint(
                id_plano_entregas, self.origem_unidade, self.unidade_autorizadora
            )
        assert endpoint == mock_get_endpoint.return_value
        mock_get_endpoint.assert_called_once_with(
            constants_endpoints.PLANO_ENTREGAS_ENDPOINT,
            origem_unidade=self.origem_unidade,
            cod_unidade_autorizadora=self.unidade_autorizadora,
            id_plano_entregas=id_plano_entregas,
        )

    def test_plano_trabalho_endpoint_deveria_estar_corretamente_definido(self):
        id_plano_trabalho = 123
        with mock.patch(
            "api_pgd_client.client.ApiClient.get_endpoint"
        ) as mock_get_endpoint:
            endpoint = self.api_client.plano_trabalho_endpoint(id_plano_trabalho)
        assert endpoint == mock_get_endpoint.return_value
        mock_get_endpoint.assert_called_once_with(
            constants_endpoints.PLANO_TRABALHO_ENDPOINT,
            origem_unidade=self.origem_unidade,
            cod_unidade_autorizadora=self.unidade_autorizadora,
            id_plano_trabalho=id_plano_trabalho,
        )

    def test_plano_trabalho_endpoint_deveria_estar_corretamente_definido_com_valores_proprios(
        self,
    ):
        id_plano_trabalho = 123
        api_client = client.ApiClient(
            origem_unidade="Nenhum", cod_unidade_autorizadora="000"
        )
        with mock.patch(
            "api_pgd_client.client.ApiClient.get_endpoint"
        ) as mock_get_endpoint:
            endpoint = api_client.plano_trabalho_endpoint(
                id_plano_trabalho, self.origem_unidade, self.unidade_autorizadora
            )
        assert endpoint == mock_get_endpoint.return_value
        mock_get_endpoint.assert_called_once_with(
            constants_endpoints.PLANO_TRABALHO_ENDPOINT,
            origem_unidade=self.origem_unidade,
            cod_unidade_autorizadora=self.unidade_autorizadora,
            id_plano_trabalho=id_plano_trabalho,
        )

    def test_participante_endpoint_deveria_estar_corretamente_definido(self):
        with mock.patch(
            "api_pgd_client.client.ApiClient.get_endpoint"
        ) as mock_get_endpoint:
            endpoint = self.api_client.participante_endpoint(
                self.unidade_lotacao, self.matricula
            )
        assert endpoint == mock_get_endpoint.return_value
        mock_get_endpoint.assert_called_once_with(
            constants_endpoints.PARTICIPANTE_ENDPOINT,
            origem_unidade=self.origem_unidade,
            cod_unidade_autorizadora=self.unidade_autorizadora,
            cod_unidade_lotacao=self.unidade_lotacao,
            matricula_siape=self.matricula,
        )

    def test_participante_endpoint_deveria_estar_corretamente_definido_com_valores_proprios(
        self,
    ):
        api_client = client.ApiClient(
            origem_unidade="Nenhum", cod_unidade_autorizadora="000"
        )
        with mock.patch(
            "api_pgd_client.client.ApiClient.get_endpoint"
        ) as mock_get_endpoint:
            endpoint = api_client.participante_endpoint(
                self.unidade_lotacao,
                self.matricula,
                self.origem_unidade,
                self.unidade_autorizadora,
            )
        assert endpoint == mock_get_endpoint.return_value
        mock_get_endpoint.assert_called_once_with(
            constants_endpoints.PARTICIPANTE_ENDPOINT,
            origem_unidade=self.origem_unidade,
            cod_unidade_autorizadora=self.unidade_autorizadora,
            cod_unidade_lotacao=self.unidade_lotacao,
            matricula_siape=self.matricula,
        )

    def test_propriedade_token_deveria_buscar_um_novo_token(self):
        with mock.patch("api_pgd_client.client.ApiClient.get_token") as mock_get_token:
            token = self.api_client.token
        mock_get_token.assert_called_once_with()
        assert token == mock_get_token.return_value

    def test_propriedade_token_deveria_ser_reutilizada_quando_ja_existir(self):
        token_esperado = {
            "access_token": "token",
            "type": "Bearer",
        }
        self.api_client._token = token_esperado
        with mock.patch("api_pgd_client.client.ApiClient.get_token") as mock_get_token:
            token = self.api_client.token
        mock_get_token.assert_not_called()
        assert token == token_esperado

    def test_get_token_deveria_retornar_um_token(self):
        with mock.patch("api_pgd_client.client.ApiClient.do_post") as mock_do_post:
            token = self.api_client.get_token()
        assert token == mock_do_post.return_value

    def test_get_token_deveria_chamar_o_endpoint_token_corretamente(self):
        with mock.patch("api_pgd_client.client.ApiClient.do_post") as mock_do_post:
            self.api_client.get_token()
        mock_do_post.assert_called_once_with(
            self.api_client.token_endpoint,
            {
                "username": constants.API_USERNAME,
                "password": constants.API_PASSWORD,
            },
            {
                constants_headers.CONTENT_TYPE_FORM_URLENCODED_HEADER.name: constants_headers.CONTENT_TYPE_FORM_URLENCODED_HEADER.value
            },
            as_json=False,
        )

    def test_consultar_usuario_deveria_chamar_o_endpoint_user_corretamente(
        self,
    ):
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_get") as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.user_endpoint"
            ) as mock_user_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.consultar_usuario(self.email)
        mock_do_get.assert_called_once_with(
            mock_user_endpoint.return_value,
            {},
            mock_default_headers.return_value,
        )
        mock_user_endpoint.assert_called_once_with(self.email)

    def test_consultar_usuario_deveria_tentar_novamente_quando_token_invalido(
        self,
    ):
        api_client = client.ApiClient()
        sucesso_esperado = {"email": self.email, "origem_unidade": self.origem_unidade}
        do_get_side_effects = [
            client.ApiClient.Error(constants_errors.TOKEN_INVALIDO),
            sucesso_esperado,
        ]
        with (
            mock.patch(
                "api_pgd_client.client.ApiClient.do_get",
                side_effect=do_get_side_effects,
            ) as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.user_endpoint"
            ) as mock_user_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
            mock.patch("api_pgd_client.client.ApiClient.get_token"),
        ):
            resultado = api_client.consultar_usuario(self.email)

        assert 2 == mock_do_get.call_count
        mock_do_get.assert_has_calls(
            [
                mock.call(
                    mock_user_endpoint.return_value,
                    {},
                    mock_default_headers.return_value,
                ),
                mock.call(
                    mock_user_endpoint.return_value,
                    {},
                    mock_default_headers.return_value,
                ),
            ]
        )
        assert resultado == entities.User(**sucesso_esperado)

    def test_consultar_participante_deveria_chamar_o_endpoint_participante_corretamente(
        self,
    ):
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_get") as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.participante_endpoint"
            ) as mock_participante_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.consultar_participante(self.unidade_lotacao, self.matricula)
        mock_do_get.assert_called_once_with(
            mock_participante_endpoint.return_value,
            {},
            mock_default_headers.return_value,
        )
        mock_participante_endpoint.assert_called_once_with(
            self.unidade_lotacao, self.matricula, "", 0
        )

    def test_consultar_participante_deveria_chamar_o_endpoint_participante_corretamente_com_valores_proprios(
        self,
    ):
        params = [
            self.unidade_lotacao,
            self.matricula,
            self.origem_unidade,
            self.unidade_autorizadora,
        ]
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_get") as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.participante_endpoint"
            ) as mock_participante_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.consultar_participante(*params)
        mock_do_get.assert_called_once_with(
            mock_participante_endpoint.return_value,
            {},
            mock_default_headers.return_value,
        )
        mock_participante_endpoint.assert_called_once_with(*params)

    def test_consultar_participante_deveria_tentar_novamente_quando_token_invalido(
        self,
    ):
        api_client = client.ApiClient()
        sucesso_esperado = {
            "cod_unidade_lotacao": self.unidade_lotacao,
            "matricula_siape": self.matricula,
        }
        do_get_side_effects = [
            client.ApiClient.Error(constants_errors.TOKEN_INVALIDO),
            sucesso_esperado,
        ]
        with (
            mock.patch(
                "api_pgd_client.client.ApiClient.do_get",
                side_effect=do_get_side_effects,
            ) as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.participante_endpoint"
            ) as mock_participante_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
            mock.patch("api_pgd_client.client.ApiClient.get_token"),
        ):
            resultado = api_client.consultar_participante(
                self.unidade_lotacao, self.matricula
            )

        assert 2 == mock_do_get.call_count
        mock_do_get.assert_has_calls(
            [
                mock.call(
                    mock_participante_endpoint.return_value,
                    {},
                    mock_default_headers.return_value,
                ),
                mock.call(
                    mock_participante_endpoint.return_value,
                    {},
                    mock_default_headers.return_value,
                ),
            ]
        )
        assert resultado == entities.Participante(**sucesso_esperado)

    def test_enviar_participante_deveria_chamar_o_endpoint_participante_corretamente(
        self,
    ):
        participante_params = {
            "cod_unidade_lotacao": self.unidade_lotacao,
            "matricula_siape": self.matricula,
            "origem_unidade": self.origem_unidade,
            "cod_unidade_autorizadora": self.unidade_autorizadora,
        }
        participante = entities.Participante(**participante_params)
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_put") as mock_do_put,
            mock.patch(
                "api_pgd_client.client.ApiClient.participante_endpoint"
            ) as mock_participante_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.enviar_participante(participante)
        mock_do_put.assert_called_once_with(
            mock_participante_endpoint.return_value,
            participante.to_dict(),
            mock_default_headers.return_value,
        )
        mock_participante_endpoint.assert_called_once_with(
            self.unidade_lotacao,
            self.matricula,
            self.origem_unidade,
            self.unidade_autorizadora,
        )

    def test_enviar_participante_deveria_tentar_novamente_quando_token_invalido(
        self,
    ):
        api_client = client.ApiClient()
        participante_params = {
            "cod_unidade_lotacao": self.unidade_lotacao,
            "matricula_siape": self.matricula,
            "origem_unidade": self.origem_unidade,
            "cod_unidade_autorizadora": self.unidade_autorizadora,
        }
        participante = entities.Participante(**participante_params)
        do_get_side_effects = [
            client.ApiClient.Error(constants_errors.TOKEN_INVALIDO),
            participante_params,
        ]
        with (
            mock.patch(
                "api_pgd_client.client.ApiClient.do_put",
                side_effect=do_get_side_effects,
            ) as mock_do_put,
            mock.patch(
                "api_pgd_client.client.ApiClient.participante_endpoint"
            ) as mock_participante_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
            mock.patch("api_pgd_client.client.ApiClient.get_token"),
        ):
            resultado = api_client.enviar_participante(participante)

        assert 2 == mock_do_put.call_count
        call_params = [
            mock_participante_endpoint.return_value,
            participante.to_dict(),
            mock_default_headers.return_value,
        ]
        mock_do_put.assert_has_calls([mock.call(*call_params), mock.call(*call_params)])
        assert resultado == participante_params

    def test_consultar_plano_entregas_deveria_chamar_o_endpoint_plano_entregas_corretamente(
        self,
    ):
        id_plano_entregas = 555
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_get") as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_entregas_endpoint"
            ) as mock_plano_entregas_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.consultar_plano_entregas(id_plano_entregas)
        mock_do_get.assert_called_once_with(
            mock_plano_entregas_endpoint.return_value,
            {},
            mock_default_headers.return_value,
        )
        mock_plano_entregas_endpoint.assert_called_once_with(id_plano_entregas, "", 0)

    def test_consultar_plano_entregas_deveria_chamar_o_endpoint_plano_entregas_corretamente_com_valores_proprios(
        self,
    ):
        id_plano_entregas = 555
        params = [id_plano_entregas, self.origem_unidade, self.unidade_autorizadora]
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_get") as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_entregas_endpoint"
            ) as mock_plano_entregas_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.consultar_plano_entregas(*params)
        mock_do_get.assert_called_once_with(
            mock_plano_entregas_endpoint.return_value,
            {},
            mock_default_headers.return_value,
        )
        mock_plano_entregas_endpoint.assert_called_once_with(*params)

    def test_consultar_plano_entregas_deveria_tentar_novamente_quando_token_invalido(
        self,
    ):
        api_client = client.ApiClient()
        id_plano_entregas = 555
        sucesso_esperado = {
            "cod_unidade_executora": 10,
            "id_plano_entregas": id_plano_entregas,
        }
        do_get_side_effects = [
            client.ApiClient.Error(constants_errors.TOKEN_INVALIDO),
            sucesso_esperado,
        ]
        with (
            mock.patch(
                "api_pgd_client.client.ApiClient.do_get",
                side_effect=do_get_side_effects,
            ) as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_entregas_endpoint"
            ) as mock_plano_entregas_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
            mock.patch("api_pgd_client.client.ApiClient.get_token"),
        ):
            resultado = api_client.consultar_plano_entregas(id_plano_entregas)

        assert 2 == mock_do_get.call_count
        mock_do_get.assert_has_calls(
            [
                mock.call(
                    mock_plano_entregas_endpoint.return_value,
                    {},
                    mock_default_headers.return_value,
                ),
                mock.call(
                    mock_plano_entregas_endpoint.return_value,
                    {},
                    mock_default_headers.return_value,
                ),
            ]
        )
        assert resultado == entities.PlanoDeEntregas(**sucesso_esperado)

    def test_enviar_plano_entregas_deveria_chamar_o_endpoint_plano_entregas_corretamente(
        self,
    ):
        id_plano_entregas = 555
        plano_entregas_params = {
            "origem_unidade": self.origem_unidade,
            "cod_unidade_autorizadora": self.unidade_autorizadora,
            "id_plano_entregas": id_plano_entregas,
        }
        plano_entregas = entities.PlanoDeEntregas(**plano_entregas_params)
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_put") as mock_do_put,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_entregas_endpoint"
            ) as mock_plano_entregas_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.enviar_plano_entregas(plano_entregas)
        mock_do_put.assert_called_once_with(
            mock_plano_entregas_endpoint.return_value,
            plano_entregas.to_dict(),
            mock_default_headers.return_value,
        )
        mock_plano_entregas_endpoint.assert_called_once_with(
            id_plano_entregas, self.origem_unidade, self.unidade_autorizadora
        )

    def test_enviar_plano_entregas_deveria_tentar_novamente_quando_token_invalido(
        self,
    ):
        api_client = client.ApiClient()
        id_plano_entregas = 555
        plano_entregas_params = {
            "origem_unidade": self.origem_unidade,
            "cod_unidade_autorizadora": self.unidade_autorizadora,
            "id_plano_entregas": id_plano_entregas,
        }
        plano_entregas = entities.PlanoDeEntregas(**plano_entregas_params)
        do_get_side_effects = [
            client.ApiClient.Error(constants_errors.TOKEN_INVALIDO),
            plano_entregas_params,
        ]
        with (
            mock.patch(
                "api_pgd_client.client.ApiClient.do_put",
                side_effect=do_get_side_effects,
            ) as mock_do_put,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_entregas_endpoint"
            ) as mock_plano_entregas_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
            mock.patch("api_pgd_client.client.ApiClient.get_token"),
        ):
            resultado = api_client.enviar_plano_entregas(plano_entregas)

        assert 2 == mock_do_put.call_count
        call_params = [
            mock_plano_entregas_endpoint.return_value,
            plano_entregas.to_dict(),
            mock_default_headers.return_value,
        ]
        mock_do_put.assert_has_calls([mock.call(*call_params), mock.call(*call_params)])
        assert resultado == plano_entregas_params

    def test_consultar_plano_trabalho_deveria_chamar_o_endpoint_plano_trabalho_corretamente(
        self,
    ):
        id_plano_trabalho = 555
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_get") as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_trabalho_endpoint"
            ) as mock_plano_trabalho_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.consultar_plano_trabalho(id_plano_trabalho)
        mock_do_get.assert_called_once_with(
            mock_plano_trabalho_endpoint.return_value,
            {},
            mock_default_headers.return_value,
        )
        mock_plano_trabalho_endpoint.assert_called_once_with(id_plano_trabalho, "", 0)

    def test_consultar_plano_trabalho_deveria_chamar_o_endpoint_plano_trabalho_corretamente_com_valores_proprios(
        self,
    ):
        id_plano_trabalho = 555
        params = [id_plano_trabalho, self.origem_unidade, self.unidade_autorizadora]
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_get") as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_trabalho_endpoint"
            ) as mock_plano_trabalho_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.consultar_plano_trabalho(*params)
        mock_do_get.assert_called_once_with(
            mock_plano_trabalho_endpoint.return_value,
            {},
            mock_default_headers.return_value,
        )
        mock_plano_trabalho_endpoint.assert_called_once_with(*params)

    def test_consultar_plano_trabalho_deveria_tentar_novamente_quando_token_invalido(
        self,
    ):
        api_client = client.ApiClient()
        id_plano_trabalho = 555
        sucesso_esperado = {
            "cod_unidade_executora": 10,
            "id_plano_trabalho": id_plano_trabalho,
        }
        do_get_side_effects = [
            client.ApiClient.Error(constants_errors.TOKEN_INVALIDO),
            sucesso_esperado,
        ]
        with (
            mock.patch(
                "api_pgd_client.client.ApiClient.do_get",
                side_effect=do_get_side_effects,
            ) as mock_do_get,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_trabalho_endpoint"
            ) as mock_plano_trabalho_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
            mock.patch("api_pgd_client.client.ApiClient.get_token"),
        ):
            resultado = api_client.consultar_plano_trabalho(id_plano_trabalho)

        assert 2 == mock_do_get.call_count
        mock_do_get.assert_has_calls(
            [
                mock.call(
                    mock_plano_trabalho_endpoint.return_value,
                    {},
                    mock_default_headers.return_value,
                ),
                mock.call(
                    mock_plano_trabalho_endpoint.return_value,
                    {},
                    mock_default_headers.return_value,
                ),
            ]
        )
        assert resultado == entities.PlanoDeTrabalho(**sucesso_esperado)

    def test_enviar_plano_trabalho_deveria_chamar_o_endpoint_plano_trabalho_corretamente(
        self,
    ):
        id_plano_trabalho = 555
        plano_trabalho_params = {
            "origem_unidade": self.origem_unidade,
            "cod_unidade_autorizadora": self.unidade_autorizadora,
            "id_plano_trabalho": id_plano_trabalho,
        }
        plano_trabalho = entities.PlanoDeTrabalho(**plano_trabalho_params)
        with (
            mock.patch("api_pgd_client.client.ApiClient.do_put") as mock_do_put,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_trabalho_endpoint"
            ) as mock_plano_trabalho_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
        ):
            self.api_client.enviar_plano_trabalho(plano_trabalho)
        mock_do_put.assert_called_once_with(
            mock_plano_trabalho_endpoint.return_value,
            plano_trabalho.to_dict(),
            mock_default_headers.return_value,
        )
        mock_plano_trabalho_endpoint.assert_called_once_with(
            id_plano_trabalho,
            self.origem_unidade,
            self.unidade_autorizadora,
        )

    def test_enviar_plano_trabalho_deveria_tentar_novamente_quando_token_invalido(
        self,
    ):
        api_client = client.ApiClient()
        id_plano_trabalho = 555
        plano_trabalho_params = {
            "origem_unidade": self.origem_unidade,
            "cod_unidade_autorizadora": self.unidade_autorizadora,
            "id_plano_trabalho": id_plano_trabalho,
        }
        plano_trabalho = entities.PlanoDeTrabalho(**plano_trabalho_params)
        do_get_side_effects = [
            client.ApiClient.Error(constants_errors.TOKEN_INVALIDO),
            plano_trabalho_params,
        ]
        with (
            mock.patch(
                "api_pgd_client.client.ApiClient.do_put",
                side_effect=do_get_side_effects,
            ) as mock_do_put,
            mock.patch(
                "api_pgd_client.client.ApiClient.plano_trabalho_endpoint"
            ) as mock_plano_trabalho_endpoint,
            mock.patch(
                "api_pgd_client.client.ApiClient.default_headers",
                new_callable=mock.PropertyMock,
            ) as mock_default_headers,
            mock.patch("api_pgd_client.client.ApiClient.get_token"),
        ):
            resultado = api_client.enviar_plano_trabalho(plano_trabalho)

        assert 2 == mock_do_put.call_count
        call_params = [
            mock_plano_trabalho_endpoint.return_value,
            plano_trabalho.to_dict(),
            mock_default_headers.return_value,
        ]
        mock_do_put.assert_has_calls([mock.call(*call_params), mock.call(*call_params)])
        assert resultado == plano_trabalho_params

    def test_retry_on_expired_token_nao_deveria_reexecutar_o_metodo_quando_token_valido(
        self,
    ):
        sucesso_esperado = {"detail": "Sucesso"}
        mock_method = mock.Mock(return_value=sucesso_esperado)
        with mock.patch("api_pgd_client.client.ApiClient.get_token"):
            resultado = self.api_client.retry_on_expired_token(mock_method)
        mock_method.assert_called_once()
        assert sucesso_esperado == resultado

    def test_retry_on_expired_token_deveria_reexecutar_o_metodo_quando_token_invalido(
        self,
    ):
        sucesso_esperado = {"detail": "Sucesso"}
        side_effects = [
            client.ApiClient.Error(constants_errors.TOKEN_INVALIDO),
            sucesso_esperado,
        ]
        mock_method = mock.Mock(side_effect=side_effects)
        with mock.patch("api_pgd_client.client.ApiClient.get_token"):
            resultado = self.api_client.retry_on_expired_token(mock_method)
        assert 2 == mock_method.call_count
        assert sucesso_esperado == resultado

    def test_retry_on_expired_token_deveria_lancar_erro(self):
        mock_method = mock.Mock(side_effect=client.ApiClient.Error("Erro genérico"))
        with pytest.raises(client.ApiClient.Error, match="Erro genérico"):
            self.api_client.retry_on_expired_token(mock_method)
        mock_method.assert_called_once()

    def test_sss(self):
        pass
