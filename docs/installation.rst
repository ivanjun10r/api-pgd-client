.. highlight:: shell

============
Instalação
============


Requisitos
----------

* Python 3.9 ou superior
* pip


Versão estável
--------------

Para instalar a versão mais recente disponível no PyPI, execute:

.. code-block:: console

    $ pip install api_pgd_client

Recomenda-se o uso de um ambiente virtual para isolar as dependências:

.. code-block:: console

    $ python -m venv .venv
    $ source .venv/bin/activate    # Linux / macOS
    $ .venv\Scripts\activate       # Windows

    $ pip install api_pgd_client


Configuração do ambiente
------------------------

A biblioteca lê suas configurações via variáveis de ambiente (usando ``python-decouple``),
compatível com arquivos ``.env``. Crie um arquivo ``.env`` na raiz do seu projeto:

.. code-block:: ini

    # Obrigatórias
    PGD_API_USERNAME=seu_usuario
    PGD_API_PASSWORD=sua_senha
    PGD_SOURCE_SYSTEM_NAME=NomeDoSeuSistema
    PGD_SOURCE_SYSTEM_VERSION=1.0.0

    # Opcionais
    PGD_API_URL=https://api-pgd.dth.api.gov.br/
    PGD_SOURCE_SYSTEM_ABOUT_URL=https://meu-sistema.gov.br
    PGD_API_REQUEST_TIMEOUT=300

.. note::

   O arquivo ``.env`` **não deve** ser versionado. Adicione-o ao ``.gitignore``.


A partir do código-fonte (desenvolvimento)
------------------------------------------

Este projeto usa `uv`_ para gerenciar dependências e ambientes virtuais.

1. Clone o repositório:

.. code-block:: console

    $ git clone https://github.com/ivanjun10r/api_pgd_client.git
    $ cd api_pgd_client

2. Instale o uv (caso ainda não tenha):

.. code-block:: console

    $ curl -LsSf https://astral.sh/uv/install.sh | sh

3. Crie o ambiente virtual e instale todas as dependências:

.. code-block:: console

    $ uv sync --all-groups

4. Configure o pre-commit:

.. code-block:: console

    $ uv run pre-commit install

5. Crie um arquivo ``.env`` na raiz do projeto com as variáveis necessárias (ver seção
   :ref:`Configuração do ambiente <configuração-do-ambiente>` acima).

A partir daí o ambiente está pronto para execução de testes e implementação de novas funcionalidades.


.. _uv: https://docs.astral.sh/uv/
.. _Github repo: https://github.com/ivanjun10r/api_pgd_client
