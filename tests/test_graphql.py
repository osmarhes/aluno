import unittest

from aluno.model import Aluno
from tests.base import ServidorTestCase

CRIAR = """
mutation ($input: AlunoInput!) {
  criarAluno(input: $input) { id nome idade }
}
"""

ATUALIZAR = """
mutation ($id: ID!, $input: AlunoInput!) {
  atualizarAluno(id: $id, input: $input) { id nome idade }
}
"""


class GraphQLTest(ServidorTestCase):

    def test_criar_e_listar(self):
        status, resp = self.graphql(CRIAR, {"input": {"nome": "Aline", "idade": 10}})
        self.assertEqual(status, 200)
        self.assertEqual(resp, {"data": {"criarAluno": {"id": "1", "nome": "Aline", "idade": 10}}})

        _, resp = self.graphql("{ alunos { nome } }")
        self.assertEqual(resp, {"data": {"alunos": [{"nome": "Aline"}]}})

    def test_buscar_por_id(self):
        aluno = self.repository.inserir(Aluno(None, "Clara", 12))

        _, resp = self.graphql("query ($id: ID!) { aluno(id: $id) { nome idade } }", {"id": aluno.id})
        self.assertEqual(resp, {"data": {"aluno": {"nome": "Clara", "idade": 12}}})

        _, resp = self.graphql('{ aluno(id: "99") { nome } }')
        self.assertEqual(resp, {"data": {"aluno": None}})

    def test_atualizar(self):
        aluno = self.repository.inserir(Aluno(None, "Clara", 10))

        _, resp = self.graphql(ATUALIZAR, {"id": aluno.id, "input": {"nome": "Clara Put", "idade": 12}})

        self.assertEqual(resp["data"]["atualizarAluno"], {"id": str(aluno.id), "nome": "Clara Put", "idade": 12})
        self.assertEqual(self.repository.buscar(aluno.id), Aluno(aluno.id, "Clara Put", 12))

    def test_atualizar_inexistente(self):
        _, resp = self.graphql(ATUALIZAR, {"id": "20", "input": {"nome": "Aline", "idade": 10}})

        self.assertIsNone(resp["data"])
        self.assertEqual(resp["errors"][0]["extensions"], {"code": "NOT_FOUND"})

    def test_remover(self):
        aluno = self.repository.inserir(Aluno(None, "Jorge", 10))

        _, resp = self.graphql(f'mutation {{ removerAluno(id: "{aluno.id}") }}')

        self.assertEqual(resp, {"data": {"removerAluno": str(aluno.id)}})
        self.assertIsNone(self.repository.buscar(aluno.id))

    def test_nome_em_branco(self):
        _, resp = self.graphql(CRIAR, {"input": {"nome": " ", "idade": 10}})

        self.assertEqual(
            resp["errors"][0]["extensions"],
            {"code": "VALIDATION", "campos": {"nome": "Nome é requerido"}},
        )

    def test_idade_ausente_rejeitada_pelo_schema(self):
        _, resp = self.graphql(CRIAR, {"input": {"nome": "Aline"}})

        self.assertIsNone(resp["data"])
        self.assertIn("idade", resp["errors"][0]["message"])
        self.assertEqual(self.repository.listar(), [])

    def test_campo_inexistente(self):
        status, resp = self.graphql("{ alunos { email } }")

        self.assertEqual(status, 400)
        self.assertNotIn("data", resp)

    def test_id_invalido(self):
        _, resp = self.graphql('{ aluno(id: "abc") { nome } }')
        self.assertEqual(resp["errors"][0]["extensions"], {"code": "BAD_USER_INPUT"})

    def test_query_com_erro_de_sintaxe(self):
        status, resp = self.graphql("{ alunos { ")
        self.assertEqual(status, 400)

    def test_sem_query(self):
        status, _ = self.requisitar("POST", "/graphql", {})
        self.assertEqual(status, 400)

    def test_graphiql(self):
        status, corpo = self.requisitar("GET", "/graphql")
        self.assertEqual(status, 200)
        self.assertIn("GraphiQL", corpo)


if __name__ == "__main__":
    unittest.main()
