package br.com.osmarhes.aluno.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import br.com.osmarhes.aluno.model.Aluno;

@Repository
public interface AlunoRepository extends JpaRepository<Aluno, Long>{

}
