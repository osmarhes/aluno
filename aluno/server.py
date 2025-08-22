"""Servidor HTTP (stdlib) expondo a API REST em /aluno e GraphQL em /graphql."""

import json
import logging
import re
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from aluno.model import AlunoNaoEncontrado, ValidacaoError
from aluno.schema import executar
from aluno.service import AlunoService

log = logging.getLogger("aluno")

ROTA_ALUNO_ID = re.compile(r"^/aluno/(\d+)$")

# Interface GraphiQL para explorar a API pelo navegador (substitui o Swagger UI).
GRAPHIQL_HTML = """<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <title>Aluno - GraphiQL</title>
  <style>body { margin: 0; height: 100vh; } #graphiql { height: 100vh; }</style>
  <link rel="stylesheet" href="https://unpkg.com/graphiql@3.0.6/graphiql.min.css">
</head>
<body>
  <div id="graphiql">Carregando...</div>
  <script crossorigin src="https://unpkg.com/react@18.2.0/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18.2.0/umd/react-dom.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/graphiql@3.0.6/graphiql.min.js"></script>
  <script>
    const fetcher = GraphiQL.createFetcher({ url: "/graphql" });
    ReactDOM.createRoot(document.getElementById("graphiql"))
      .render(React.createElement(GraphiQL, { fetcher }));
  </script>
</body>
</html>
"""


class RequisicaoInvalida(Exception):
    pass


class AlunoHandler(BaseHTTPRequestHandler):
    server_version = "Aluno/0.0.1"

    @property
    def service(self) -> AlunoService:
        return self.server.service

    @property
    def caminho(self) -> str:
        return urlsplit(self.path).path.rstrip("/") or "/"

    def do_GET(self):
        if self.caminho == "/aluno":
            self._json(HTTPStatus.OK, [asdict(a) for a in self.service.listar()])
        elif self.caminho == "/graphql":
            self._enviar(HTTPStatus.OK, GRAPHIQL_HTML, "text/html; charset=utf-8")
        else:
            self._nao_encontrado()

    def do_POST(self):
        if self.caminho == "/aluno":
            self._tratar(self._criar_aluno)
        elif self.caminho == "/graphql":
            self._tratar(self._graphql)
        else:
            self._nao_encontrado()

    def do_PUT(self):
        if self.caminho == "/aluno":
            self._tratar(self._atualizar_aluno)
        else:
            self._nao_encontrado()

    def do_DELETE(self):
        rota = ROTA_ALUNO_ID.match(self.caminho)
        if rota:
            self._tratar(lambda: self._remover_aluno(int(rota.group(1))))
        else:
            self._nao_encontrado()

    def _criar_aluno(self):
        self.service.criar(self._ler_json())
        self._enviar(HTTPStatus.OK, "Aluno is valid")

    def _atualizar_aluno(self):
        self.service.atualizar(self._ler_json())
        self._enviar(HTTPStatus.OK, "Aluno is valid")

    def _remover_aluno(self, id_: int):
        self.service.remover(id_)
        self._enviar(HTTPStatus.OK, "Aluno is deleted")

    def _graphql(self):
        corpo = self._ler_json()
        query = corpo.get("query")
        if not isinstance(query, str):
            raise RequisicaoInvalida("Campo 'query' é requerido")
        resposta = executar(
            self.service, query, corpo.get("variables"), corpo.get("operationName")
        )
        # Sem "data" significa que a query nem chegou a executar (erro de sintaxe/validação).
        status = HTTPStatus.OK if "data" in resposta else HTTPStatus.BAD_REQUEST
        self._json(status, resposta)

    def _tratar(self, acao):
        try:
            acao()
        except ValidacaoError as e:
            self._json(HTTPStatus.CONFLICT, e.erros)
        except AlunoNaoEncontrado:
            self._enviar(HTTPStatus.NOT_FOUND, "")
        except RequisicaoInvalida as e:
            self._json(HTTPStatus.BAD_REQUEST, {"erro": str(e)})

    def _ler_json(self) -> dict:
        tamanho = int(self.headers.get("Content-Length") or 0)
        try:
            dados = json.loads(self.rfile.read(tamanho) or b"null")
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise RequisicaoInvalida("JSON inválido")
        if not isinstance(dados, dict):
            raise RequisicaoInvalida("O corpo deve ser um objeto JSON")
        return dados

    def _nao_encontrado(self):
        self._json(HTTPStatus.NOT_FOUND, {"erro": "Recurso não encontrado"})

    def _json(self, status: HTTPStatus, dados):
        self._enviar(status, json.dumps(dados, ensure_ascii=False), "application/json; charset=utf-8")

    def _enviar(self, status: HTTPStatus, corpo: str, tipo: str = "text/plain; charset=utf-8"):
        dados = corpo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def log_message(self, format, *args):
        log.info("%s - %s", self.address_string(), format % args)


def criar_servidor(host: str, porta: int, service: AlunoService) -> ThreadingHTTPServer:
    servidor = ThreadingHTTPServer((host, porta), AlunoHandler)
    servidor.service = service
    return servidor
