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

Este projeto usa `Poetry`_ para gerenciar dependências e ambientes virtuais.

1. Clone o repositório:

.. code-block:: console

    $ git clone https://github.com/ivanjun10r/api_pgd_client.git
    $ cd api_pgd_client

2. Instale o Poetry (caso ainda não tenha):

.. code-block:: console

    $ pip install poetry

3. Instale todas as dependências (produção + desenvolvimento + testes):

.. code-block:: console

    $ poetry install --with test

4. Ative o ambiente virtual criado pelo Poetry:

.. code-block:: console

    $ poetry shell

5. Configure o pre-commit:

.. code-block:: console

    $ pre-commit install

6. Crie um arquivo ``.env`` na raiz do projeto com as variáveis necessárias (ver seção
   :ref:`Configuração do ambiente <configuração-do-ambiente>` acima).

A partir daí o ambiente está pronto para execução de testes e implementação de novas funcionalidades.


.. _Poetry: https://python-poetry.org/
.. _Github repo: https://github.com/ivanjun10r/api_pgd_client
