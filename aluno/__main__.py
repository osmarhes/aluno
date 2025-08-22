"""Ponto de entrada: python -m aluno

Variáveis de ambiente:
  PORT      porta HTTP (padrão 8000)
  ALUNO_DB  arquivo SQLite (padrão ":memory:", dados perdidos ao encerrar)
"""

import logging
import os
from importlib import resources

from aluno.repository import AlunoRepository
from aluno.server import criar_servidor
from aluno.service import AlunoService


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    print(resources.files("aluno").joinpath("banner.txt").read_text(encoding="utf-8"), flush=True)

    porta = int(os.environ.get("PORT", "8000"))
    repository = AlunoRepository(os.environ.get("ALUNO_DB", ":memory:"))

    with criar_servidor("", porta, AlunoService(repository)) as servidor:
        logging.info("REST:    http://localhost:%d/aluno", porta)
        logging.info("GraphQL: http://localhost:%d/graphql", porta)
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            logging.info("Encerrando...")
        finally:
            repository.fechar()


if __name__ == "__main__":
    main()
