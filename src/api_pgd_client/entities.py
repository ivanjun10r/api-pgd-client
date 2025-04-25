import dataclasses
from typing import Any


@dataclasses.dataclass()
class BaseEntity:
    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass()
class User(BaseEntity):
    email: str = ""
    is_admin: bool = False
    disabled: bool = False
    origem_unidade: str = ""
    cod_unidade_autorizadora: int = 0
    sistema_gerador: str = ""


@dataclasses.dataclass()
class Participante(BaseEntity):
    cpf: str = ""
    matricula_siape: str = ""
    origem_unidade: str = ""
    cod_unidade_autorizadora: int = 0
    cod_unidade_lotacao: int = 0
    cod_unidade_instituidora: int = 0
    situacao: int = 0
    modalidade_execucao: int = 0
    data_assinatura_tcr: str = ""


@dataclasses.dataclass()
class PlanoDeEntregas(BaseEntity):
    origem_unidade: str = ""
    cod_unidade_autorizadora: int = 0
    cod_unidade_instituidora: int = 0
    cod_unidade_executora: int = 0
    id_plano_entregas: str = ""
    status: int = 0
    data_inicio: str = ""
    data_termino: str = ""
    avaliacao: int = 0
    data_avaliacao: str = ""
    entregas: list[dict[str, Any]] = dataclasses.field(default_factory=list)


@dataclasses.dataclass()
class Entrega(BaseEntity):
    id_entrega: str = ""
    entrega_cancelada: bool = False
    nome_entrega: str = ""
    meta_entrega: int = 0
    tipo_meta: str = "unidade"
    data_entrega: str = ""
    nome_unidade_demandante: str = ""
    nome_unidade_destinataria: str = ""


@dataclasses.dataclass()
class Contribuicao(BaseEntity):
    id_contribuicao: str = ""
    tipo_contribuicao: int = 0
    percentual_contribuicao: int = 0
    id_plano_entregas: str = ""
    id_entrega: str = ""


@dataclasses.dataclass()
class AvaliacaoRegistroExecucao(BaseEntity):
    id_periodo_avaliativo: str = ""
    data_inicio_periodo_avaliativo: str = ""
    data_fim_periodo_avaliativo: str = ""
    avaliacao_registros_execucao: int = 0
    data_avaliacao_registros_execucao: str = ""


@dataclasses.dataclass()
class PlanoDeTrabalho(BaseEntity):
    origem_unidade: str = ""
    cod_unidade_autorizadora: int = 0
    id_plano_trabalho: str = ""
    status: int = 0
    cod_unidade_executora: int = 0
    cpf_participante: str = ""
    matricula_siape: str = ""
    cod_unidade_lotacao_participante: int = 0
    data_inicio: str = ""
    data_termino: str = ""
    carga_horaria_disponivel: int = 0
    contribuicoes: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    avaliacoes_registros_execucao: list[dict[str, Any]] = dataclasses.field(
        default_factory=list
    )
