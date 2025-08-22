"""Schema GraphQL (SDL) e resolvers, delegando para o AlunoService."""

from functools import wraps

from graphql import GraphQLError, build_schema, execute, parse, validate

from aluno.model import AlunoNaoEncontrado, ValidacaoError

SDL = '''
"""Aluno cadastrado"""
type Aluno {
  id: ID!
  nome: String!
  idade: Int!
}

input AlunoInput {
  nome: String!
  idade: Int!
}

type Query {
  "Lista todos os alunos, ordenados por id"
  alunos: [Aluno!]!
  "Busca um aluno pelo id; retorna null se não existir"
  aluno(id: ID!): Aluno
}

type Mutation {
  criarAluno(input: AlunoInput!): Aluno!
  atualizarAluno(id: ID!, input: AlunoInput!): Aluno!
  "Remove o aluno e retorna o id removido"
  removerAluno(id: ID!): ID!
}
'''


def _id(valor: str) -> int:
    try:
        return int(valor)
    except ValueError:
        raise GraphQLError(f"ID inválido: {valor!r}", extensions={"code": "BAD_USER_INPUT"})


def _erros_de_dominio(resolver):
    """Converte exceções do domínio em GraphQLError com `extensions.code`."""

    @wraps(resolver)
    def wrapper(obj, info, **args):
        try:
            return resolver(obj, info, **args)
        except ValidacaoError as e:
            raise GraphQLError(
                "Dados inválidos", extensions={"code": "VALIDATION", "campos": e.erros}
            )
        except AlunoNaoEncontrado as e:
            raise GraphQLError(
                f"Aluno {e.args[0]} não encontrado", extensions={"code": "NOT_FOUND"}
            )

    return wrapper


def _service(info):
    return info.context["service"]


def resolve_alunos(obj, info):
    return _service(info).listar()


@_erros_de_dominio
def resolve_aluno(obj, info, id):
    try:
        return _service(info).buscar(_id(id))
    except AlunoNaoEncontrado:
        return None


@_erros_de_dominio
def resolve_criar_aluno(obj, info, input):
    return _service(info).criar(input)


@_erros_de_dominio
def resolve_atualizar_aluno(obj, info, id, input):
    return _service(info).atualizar({**input, "id": _id(id)})


@_erros_de_dominio
def resolve_remover_aluno(obj, info, id):
    _service(info).remover(_id(id))
    return id


def _criar_schema():
    schema = build_schema(SDL)
    resolvers = {
        schema.query_type: {"alunos": resolve_alunos, "aluno": resolve_aluno},
        schema.mutation_type: {
            "criarAluno": resolve_criar_aluno,
            "atualizarAluno": resolve_atualizar_aluno,
            "removerAluno": resolve_remover_aluno,
        },
    }
    for tipo, campos in resolvers.items():
        for campo, resolver in campos.items():
            tipo.fields[campo].resolve = resolver
    return schema


SCHEMA = _criar_schema()


def executar(service, query: str, variables: dict | None = None, operation_name: str | None = None) -> dict:
    """Executa a operação. Erros de sintaxe/validação retornam sem "data", conforme a spec."""
    try:
        documento = parse(query)
    except GraphQLError as e:
        return {"errors": [e.formatted]}

    erros = validate(SCHEMA, documento)
    if erros:
        return {"errors": [e.formatted for e in erros]}

    resultado = execute(
        SCHEMA,
        documento,
        variable_values=variables,
        operation_name=operation_name,
        context_value={"service": service},
    )
    return resultado.formatted
