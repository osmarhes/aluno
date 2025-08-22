import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from aluno.repository import AlunoRepository
from aluno.server import criar_servidor
from aluno.service import AlunoService


class ServidorTestCase(unittest.TestCase):
    """Sobe um servidor em porta aleatória com banco em memória isolado por teste."""

    def setUp(self):
        self.repository = AlunoRepository(":memory:")
        self.servidor = criar_servidor("127.0.0.1", 0, AlunoService(self.repository))
        self.base = f"http://127.0.0.1:{self.servidor.server_address[1]}"
        threading.Thread(target=self.servidor.serve_forever, args=(0.05,), daemon=True).start()

    def tearDown(self):
        self.servidor.shutdown()
        self.servidor.server_close()
        self.repository.fechar()

    def requisitar(self, metodo: str, caminho: str, corpo=None) -> tuple[int, str]:
        dados = json.dumps(corpo).encode() if corpo is not None else None
        req = Request(self.base + caminho, data=dados, method=metodo,
                      headers={"Content-Type": "application/json"})
        try:
            with urlopen(req) as resp:
                return resp.status, resp.read().decode()
        except HTTPError as e:
            return e.code, e.read().decode()

    def graphql(self, query: str, variables: dict | None = None) -> tuple[int, dict]:
        status, corpo = self.requisitar("POST", "/graphql", {"query": query, "variables": variables})
        return status, json.loads(corpo)
