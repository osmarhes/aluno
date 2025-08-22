import sqlite3
import threading

from aluno.model import Aluno

SCHEMA = """
CREATE TABLE IF NOT EXISTS aluno (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT    NOT NULL,
    idade INTEGER NOT NULL
)
"""


class AlunoRepository:
    """Acesso ao SQLite. Uma conexão compartilhada entre threads, protegida por lock."""

    def __init__(self, caminho: str = ":memory:"):
        self._conn = sqlite3.connect(caminho, check_same_thread=False)
        self._lock = threading.Lock()
        with self._lock, self._conn:
            self._conn.execute(SCHEMA)

    def listar(self) -> list[Aluno]:
        with self._lock:
            linhas = self._conn.execute("SELECT id, nome, idade FROM aluno ORDER BY id").fetchall()
        return [Aluno(*linha) for linha in linhas]

    def buscar(self, id_: int) -> Aluno | None:
        with self._lock:
            linha = self._conn.execute(
                "SELECT id, nome, idade FROM aluno WHERE id = ?", (id_,)
            ).fetchone()
        return Aluno(*linha) if linha else None

    def inserir(self, aluno: Aluno) -> Aluno:
        with self._lock, self._conn:
            cursor = self._conn.execute(
                "INSERT INTO aluno (nome, idade) VALUES (?, ?)", (aluno.nome, aluno.idade)
            )
        return Aluno(cursor.lastrowid, aluno.nome, aluno.idade)

    def atualizar(self, aluno: Aluno) -> bool:
        with self._lock, self._conn:
            cursor = self._conn.execute(
                "UPDATE aluno SET nome = ?, idade = ? WHERE id = ?",
                (aluno.nome, aluno.idade, aluno.id),
            )
        return cursor.rowcount > 0

    def remover(self, id_: int) -> bool:
        with self._lock, self._conn:
            cursor = self._conn.execute("DELETE FROM aluno WHERE id = ?", (id_,))
        return cursor.rowcount > 0

    def fechar(self) -> None:
        self._conn.close()
