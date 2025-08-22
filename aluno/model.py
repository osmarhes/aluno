from dataclasses import dataclass


@dataclass
class Aluno:
    id: int | None
    nome: str
    idade: int


class ValidacaoError(Exception):
    """Dados inválidos; `erros` mapeia campo -> mensagem."""

    def __init__(self, erros: dict[str, str]):
        super().__init__(erros)
        self.erros = erros


class AlunoNaoEncontrado(Exception):
    pass


def _inteiro(valor) -> bool:
    return isinstance(valor, int) and not isinstance(valor, bool)


def validar(dados: dict, exigir_id: bool = False) -> Aluno:
    """Constrói um Aluno a partir de um dict, reunindo todos os erros de validação."""
    erros = {}

    id_ = dados.get("id")
    if id_ is None:
        if exigir_id:
            erros["id"] = "Id é requerido"
    elif not _inteiro(id_):
        erros["id"] = "Id deve ser um número inteiro"

    nome = dados.get("nome")
    if not isinstance(nome, str) or not nome.strip():
        erros["nome"] = "Nome é requerido"

    idade = dados.get("idade")
    if idade is None:
        erros["idade"] = "Idade é requerido"
    elif not _inteiro(idade):
        erros["idade"] = "Idade deve ser um número inteiro"

    if erros:
        raise ValidacaoError(erros)
    return Aluno(id=id_, nome=nome, idade=idade)
