from aluno.model import Aluno, AlunoNaoEncontrado, validar
from aluno.repository import AlunoRepository


class AlunoService:
    def __init__(self, repository: AlunoRepository):
        self._repository = repository

    def listar(self) -> list[Aluno]:
        return self._repository.listar()

    def buscar(self, id_: int) -> Aluno:
        aluno = self._repository.buscar(id_)
        if aluno is None:
            raise AlunoNaoEncontrado(id_)
        return aluno

    def criar(self, dados: dict) -> Aluno:
        return self._repository.inserir(validar(dados))

    def atualizar(self, dados: dict) -> Aluno:
        aluno = validar(dados, exigir_id=True)
        if not self._repository.atualizar(aluno):
            raise AlunoNaoEncontrado(aluno.id)
        return aluno

    def remover(self, id_: int) -> None:
        if not self._repository.remover(id_):
            raise AlunoNaoEncontrado(id_)
