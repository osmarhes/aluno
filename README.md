# Aluno - App teste

CRUD de alunos em Python puro (sem framework web): servidor com `http.server`,
banco SQLite (`sqlite3`) e API exposta em **REST** e **GraphQL**.

A única dependência externa é o [graphql-core](https://github.com/graphql-python/graphql-core),
implementação de referência do GraphQL em Python.

## Executando

```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m aluno
```

| Variável   | Padrão     | Descrição                                                 |
|------------|------------|-----------------------------------------------------------|
| `PORT`     | `8000`     | Porta HTTP                                                |
| `ALUNO_DB` | `:memory:` | Arquivo SQLite. Em memória, os dados somem ao encerrar.   |

Para persistir: `ALUNO_DB=alunos.db python -m aluno` (o arquivo pode ser aberto com `sqlite3 alunos.db`).

## GraphQL

GraphiQL (substitui o Swagger UI): http://localhost:8000/graphql

```graphql
mutation {
  criarAluno(input: { nome: "Aline", idade: 10 }) { id nome idade }
}

query {
  alunos { id nome idade }
  aluno(id: "1") { nome }
}

mutation {
  atualizarAluno(id: "1", input: { nome: "Aline Souza", idade: 11 }) { id nome idade }
  removerAluno(id: "1")
}
```

Erros de domínio vêm em `errors[].extensions.code`: `VALIDATION` (com `campos`),
`NOT_FOUND` e `BAD_USER_INPUT`.

## REST

Mesmo contrato da versão Spring Boot:

| Método   | Rota          | Corpo                          | Respostas                       |
|----------|---------------|--------------------------------|---------------------------------|
| `GET`    | `/aluno`      | -                              | 200 lista de alunos             |
| `POST`   | `/aluno`      | `{"nome": "...", "idade": 10}` | 200, 409 (validação)            |
| `PUT`    | `/aluno`      | `{"id": 1, "nome": ..., ...}`  | 200, 404, 409                   |
| `DELETE` | `/aluno/{id}` | -                              | 200, 404                        |

## Testes

```bash
python -m unittest -v
```

## Estrutura

```
aluno/
  model.py       entidade Aluno + validação
  repository.py  acesso ao SQLite
  service.py     regras de negócio
  schema.py      schema GraphQL (SDL) + resolvers
  server.py      rotas HTTP (REST, /graphql, GraphiQL)
  __main__.py    ponto de entrada
tests/
```
