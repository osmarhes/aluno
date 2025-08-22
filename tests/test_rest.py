import json
import unittest

from aluno.model import Aluno
from tests.base import ServidorTestCase


class RestTest(ServidorTestCase):

    def listar(self) -> list[dict]:
        status, corpo = self.requisitar("GET", "/aluno")
        self.assertEqual(status, 200)
        return json.loads(corpo)

    def test_post(self):
        status, corpo = self.requisitar("POST", "/aluno", {"nome": "Aline", "idade": 10})

        self.assertEqual((status, corpo), (200, "Aluno is valid"))
        self.assertEqual(self.listar(), [{"id": 1, "nome": "Aline", "idade": 10}])

    def test_put(self):
        aluno = self.repository.inserir(Aluno(None, "Clara", 10))

        status, _ = self.requisitar("PUT", "/aluno", {"id": aluno.id, "nome": "Clara Put", "idade": 12})

        self.assertEqual(status, 200)
        self.assertEqual(self.listar(), [{"id": aluno.id, "nome": "Clara Put", "idade": 12}])

    def test_delete(self):
        aluno = self.repository.inserir(Aluno(None, "Jorge", 10))

        status, corpo = self.requisitar("DELETE", f"/aluno/{aluno.id}")

        self.assertEqual((status, corpo), (200, "Aluno is deleted"))
        self.assertIsNone(self.repository.buscar(aluno.id))

    def test_delete_inexistente(self):
        status, _ = self.requisitar("DELETE", "/aluno/20")
        self.assertEqual(status, 404)

    def test_get_all_ordenado_por_id(self):
        self.repository.inserir(Aluno(None, "Aline", 10))
        self.repository.inserir(Aluno(None, "Clara", 12))

        self.assertEqual(
            [(a["nome"], a["idade"]) for a in self.listar()],
            [("Aline", 10), ("Clara", 12)],
        )

    def test_campos_requeridos(self):
        status, corpo = self.requisitar("POST", "/aluno", {"nome": "Aline"})
        self.assertEqual(status, 409)
        self.assertEqual(json.loads(corpo), {"idade": "Idade é requerido"})

        status, corpo = self.requisitar("POST", "/aluno", {"nome": "  ", "idade": 10})
        self.assertEqual(status, 409)
        self.assertEqual(json.loads(corpo), {"nome": "Nome é requerido"})

    def test_tipos_invalidos(self):
        status, corpo = self.requisitar("POST", "/aluno", {"nome": "Aline", "idade": "dez"})
        self.assertEqual(status, 409)
        self.assertEqual(json.loads(corpo), {"idade": "Idade deve ser um número inteiro"})

    def test_put_sem_id(self):
        status, corpo = self.requisitar("PUT", "/aluno", {"nome": "Aline", "idade": 10})
        self.assertEqual(status, 409)
        self.assertEqual(json.loads(corpo), {"id": "Id é requerido"})

    def test_put_inexistente(self):
        status, _ = self.requisitar("PUT", "/aluno", {"id": 20, "nome": "Aline", "idade": 10})
        self.assertEqual(status, 404)

    def test_json_invalido(self):
        status, _ = self.requisitar("POST", "/aluno", [1, 2])
        self.assertEqual(status, 400)

    def test_rota_inexistente(self):
        status, _ = self.requisitar("GET", "/nada")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
