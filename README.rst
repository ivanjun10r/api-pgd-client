==============
PGD API Client
==============


.. image:: https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?logo=python&logoColor=white
        :alt: Python Versions

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
        :target: https://pre-commit.com/
        :alt: pre-commit

.. image:: https://img.shields.io/badge/Linter-Ruff-brightgreen
        :target: https://github.com/astral-sh/ruff
        :alt: ruff

.. image:: https://img.shields.io/badge/mypy-enabled-blue
        :target: http://mypy-lang.org/
        :alt: mypy

.. image:: https://codecov.io/gh/ivanjun10r/api-pgd-client/graph/badge.svg?token=SJD4X6F94C
        :target: https://codecov.io/gh/ivanjun10r/api-pgd-client


Biblioteca Python para simplificar chamadas à `API do Programa de Gestão e Desempenho (PGD)`_ do
Ministério da Gestão (GovBR), que gerencia dados de teletrabalho de servidores da administração
pública federal.

* Licença: MIT
* Documentação completa: https://github.com/ivanjun10r/api_pgd_client


Instalação
----------

.. code-block:: console

    $ pip install api_pgd_client


Uso rápido
----------

Configure as variáveis de ambiente (ou um arquivo ``.env`` na raiz do projeto)::

    PGD_API_USERNAME=seu_usuario
    PGD_API_PASSWORD=sua_senha
    PGD_SOURCE_SYSTEM_NAME=MeuSistema
    PGD_SOURCE_SYSTEM_VERSION=1.0.0

Instancie o cliente e consuma a API::

    from api_pgd_client.client import ApiClient

    client = ApiClient(
        origem_unidade="SIAPE",
        cod_unidade_autorizadora=123456,
    )

    usuario = client.consultar_usuario("servidor@orgao.gov.br")

    participante = client.consultar_participante(
        cod_unidade_lotacao=123456,
        matricula_siape="1234567",
    )

    plano_entregas = client.consultar_plano_entregas("PE-2024-001")
    plano_trabalho = client.consultar_plano_trabalho("PT-2024-001")


Funcionalidades
---------------

* Autenticação OAuth2 com renovação automática de token
* Consulta e envio de **Plano de Entregas**
* Consulta e envio de **Plano de Trabalho**
* Consulta e envio de **Participantes**
* Consulta de **Usuários**
* Suporte a Python 3.9 – 3.13


Créditos
--------

Este pacote foi criado com Cookiecutter_ e o template `audreyr/cookiecutter-pypackage`_.

.. _API do Programa de Gestão e Desempenho (PGD): https://www.gov.br/servidor/pt-br/assuntos/programa-de-gestao
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
