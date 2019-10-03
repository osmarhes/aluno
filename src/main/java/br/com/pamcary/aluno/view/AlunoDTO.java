package br.com.pamcary.aluno.view;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

import br.com.pamcary.aluno.model.Aluno;
import lombok.Data;

@Data
public class AlunoDTO {
	private Long id;
    @NotBlank(message = "Nome é requerido")
	private String nome;
    @NotNull(message = "Idade é requerido")
	private Integer idade;
	
    public static AlunoDTO bind(Aluno aluno) {
    	AlunoDTO alunoDto = new AlunoDTO();
		alunoDto.setId(aluno.getId());
		alunoDto.setIdade(aluno.getIdade());
		alunoDto.setNome(aluno.getNome());
		
		return alunoDto;
	}
}
