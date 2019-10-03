package br.com.pamcary.aluno.service;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.pamcary.aluno.model.Aluno;
import br.com.pamcary.aluno.repository.AlunoRepository;
import br.com.pamcary.aluno.view.AlunoDTO;

@Service
public class AlunoService {

	@Autowired
	private AlunoRepository repository;
	
	public List<AlunoDTO> getAlunos() {
		return repository.findAll().stream().map(aluno -> AlunoDTO.bind(aluno)).collect(Collectors.toList());
	}
	
	public void save(AlunoDTO aluno) {
		repository.save(Aluno.bind(aluno));
	}
	
	public void update(AlunoDTO alunoDto) {
		Aluno aluno = repository.getOne(alunoDto.getId());
		aluno.setIdade(alunoDto.getIdade());
		aluno.setNome(alunoDto.getNome());
		repository.save(aluno);
	}
	
	public void delete(Long id) {
		repository.deleteById(id);
	}
	
	
}
