package br.com.pamcary.aluno.model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

import br.com.pamcary.aluno.view.AlunoDTO;
import lombok.Data;

@Entity
public class Aluno {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;

    @NotBlank(message = "Nome é requerido")
	private String nome;
    
    @NotNull(message = "Idade é requerido")
	private Integer idade;
	
    public static Aluno bind(AlunoDTO alunoDTO) {
		Aluno aluno = new Aluno();
		aluno.setId(alunoDTO.getId());
		aluno.setIdade(alunoDTO.getIdade());
		aluno.setNome(alunoDTO.getNome());
		
		return aluno;
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public Integer getIdade() {
		return idade;
	}

	public void setIdade(Integer idade) {
		this.idade = idade;
	}
}
