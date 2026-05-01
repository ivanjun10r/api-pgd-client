===
Uso
===

Configuração
------------

A biblioteca usa ``python-decouple`` para ler variáveis de ambiente.
Crie um arquivo ``.env`` na raiz do seu projeto com as seguintes variáveis:

+----------------------------------+--------------------------------------------------+-------------+
| Variável                         | Descrição                                        | Obrigatória |
+==================================+==================================================+=============+
| ``PGD_API_USERNAME``             | Usuário para autenticação na API                 | Sim         |
+----------------------------------+--------------------------------------------------+-------------+
| ``PGD_API_PASSWORD``             | Senha para autenticação na API                   | Sim         |
+----------------------------------+--------------------------------------------------+-------------+
| ``PGD_SOURCE_SYSTEM_NAME``       | Nome do sistema que consome a API                | Sim         |
+----------------------------------+--------------------------------------------------+-------------+
| ``PGD_SOURCE_SYSTEM_VERSION``    | Versão do sistema que consome a API              | Sim         |
+----------------------------------+--------------------------------------------------+-------------+
| ``PGD_API_URL``                  | URL base da API                                  | Não         |
+----------------------------------+--------------------------------------------------+-------------+
| ``PGD_SOURCE_SYSTEM_ABOUT_URL``  | URL de referência do sistema consumidor          | Não         |
+----------------------------------+--------------------------------------------------+-------------+
| ``PGD_API_REQUEST_TIMEOUT``      | Timeout das requisições em segundos (padrão 300) | Não         |
+----------------------------------+--------------------------------------------------+-------------+


Instanciando o cliente
----------------------

Importe e instancie a classe ``ApiClient`` com a origem da unidade e o código
da unidade autorizadora do seu contexto:

.. code-block:: python

    from api_pgd_client.client import ApiClient

    client = ApiClient(
        origem_unidade="SIAPE",           # Sigla do sistema de origem da unidade
        cod_unidade_autorizadora=123456,  # Código da unidade autorizadora
    )

O cliente realiza a autenticação automaticamente na primeira chamada e renova o
token de forma transparente sempre que este expirar.


Usuários
--------

Consultar um usuário pelo e-mail institucional:

.. code-block:: python

    usuario = client.consultar_usuario("servidor@orgao.gov.br")

    print(usuario.email)
    print(usuario.is_admin)
    print(usuario.origem_unidade)
    print(usuario.cod_unidade_autorizadora)

O retorno é uma instância de ``api_pgd_client.entities.User``.


Participantes
-------------

Consultar um participante:

.. code-block:: python

    participante = client.consultar_participante(
        cod_unidade_lotacao=123456,
        matricula_siape="1234567",
    )

    print(participante.cpf)
    print(participante.situacao)
    print(participante.modalidade_execucao)

Os parâmetros ``origem_unidade`` e ``cod_unidade_autorizadora`` são opcionais e
assumem os valores definidos na instância do cliente. Para sobrescrevê-los
pontualmente:

.. code-block:: python

    participante = client.consultar_participante(
        cod_unidade_lotacao=123456,
        matricula_siape="1234567",
        origem_unidade="SIAPE",
        cod_unidade_autorizadora=654321,
    )

Enviar (criar ou atualizar) um participante:

.. code-block:: python

    from api_pgd_client.entities import Participante

    participante = Participante(
        cpf="000.000.000-00",
        matricula_siape="1234567",
        origem_unidade="SIAPE",
        cod_unidade_autorizadora=123456,
        cod_unidade_lotacao=123456,
        cod_unidade_instituidora=123456,
        situacao=1,
        modalidade_execucao=1,
        data_assinatura_tcr="2024-01-01",
    )

    client.enviar_participante(participante)


Plano de Entregas
-----------------

Consultar um plano de entregas:

.. code-block:: python

    plano = client.consultar_plano_entregas("PE-2024-001")

    print(plano.status)
    print(plano.data_inicio)
    print(plano.data_termino)

    for entrega in plano.entregas:
        print(entrega)

Enviar um plano de entregas:

.. code-block:: python

    from api_pgd_client.entities import PlanoDeEntregas

    plano = PlanoDeEntregas(
        origem_unidade="SIAPE",
        cod_unidade_autorizadora=123456,
        cod_unidade_instituidora=123456,
        cod_unidade_executora=123456,
        id_plano_entregas="PE-2024-001",
        status=1,
        data_inicio="2024-01-01",
        data_termino="2024-12-31",
        avaliacao=0,
        data_avaliacao="",
        entregas=[],
    )

    client.enviar_plano_entregas(plano)


Plano de Trabalho
-----------------

Consultar um plano de trabalho:

.. code-block:: python

    plano = client.consultar_plano_trabalho("PT-2024-001")

    print(plano.status)
    print(plano.cpf_participante)
    print(plano.carga_horaria_disponivel)

    for contribuicao in plano.contribuicoes:
        print(contribuicao)

Enviar um plano de trabalho:

.. code-block:: python

    from api_pgd_client.entities import PlanoDeTrabalho

    plano = PlanoDeTrabalho(
        origem_unidade="SIAPE",
        cod_unidade_autorizadora=123456,
        id_plano_trabalho="PT-2024-001",
        status=1,
        cod_unidade_executora=123456,
        cpf_participante="000.000.000-00",
        matricula_siape="1234567",
        cod_unidade_lotacao_participante=123456,
        data_inicio="2024-01-01",
        data_termino="2024-12-31",
        carga_horaria_disponivel=40,
        contribuicoes=[],
        avaliacoes_registros_execucao=[],
    )

    client.enviar_plano_trabalho(plano)


Tratamento de erros
-------------------

Todas as operações levantam ``ApiClient.Error`` em caso de falha HTTP ou timeout:

.. code-block:: python

    from api_pgd_client.client import ApiClient

    client = ApiClient(origem_unidade="SIAPE", cod_unidade_autorizadora=123456)

    try:
        usuario = client.consultar_usuario("inexistente@orgao.gov.br")
    except ApiClient.Error as exc:
        print(f"Erro na chamada à API: {exc}")

O cliente renova automaticamente o token quando a API retorna erro de credenciais
inválidas, sem necessidade de intervenção manual.


Entidades disponíveis
---------------------

Todas as entidades estão no módulo ``api_pgd_client.entities`` e são implementadas
como ``dataclasses``:

+------------------------------------+-------------------------------------------------------+
| Entidade                           | Descrição                                             |
+====================================+=======================================================+
| ``User``                           | Usuário cadastrado na API                             |
+------------------------------------+-------------------------------------------------------+
| ``Participante``                   | Servidor participante do programa de gestão           |
+------------------------------------+-------------------------------------------------------+
| ``PlanoDeEntregas``                | Plano de entregas de uma unidade                      |
+------------------------------------+-------------------------------------------------------+
| ``Entrega``                        | Entrega individual dentro de um plano de entregas     |
+------------------------------------+-------------------------------------------------------+
| ``Contribuicao``                   | Contribuição de um participante a uma entrega         |
+------------------------------------+-------------------------------------------------------+
| ``AvaliacaoRegistroExecucao``      | Avaliação de período no plano de trabalho             |
+------------------------------------+-------------------------------------------------------+
| ``PlanoDeTrabalho``                | Plano de trabalho individual do servidor              |
+------------------------------------+-------------------------------------------------------+

Todas herdam de ``BaseEntity``, que expõe o método ``to_dict()`` para serialização.
