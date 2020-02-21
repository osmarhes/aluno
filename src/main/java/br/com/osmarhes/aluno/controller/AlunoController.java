package br.com.osmarhes.aluno.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.persistence.EntityNotFoundException;
import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import br.com.osmarhes.aluno.service.AlunoService;
import br.com.osmarhes.aluno.view.AlunoDTO;

@RestController
@RequestMapping("/aluno")
public class AlunoController {

	@Autowired
	private AlunoService service;
	
    @GetMapping
    public List<AlunoDTO> getAlunos() {
        return service.getAlunos();
    }
	
    @PostMapping
    public ResponseEntity<String> addAluno(@Valid @RequestBody AlunoDTO aluno) {
    	service.save(aluno);
        return ResponseEntity.ok("Aluno is valid");
    }
    
    @PutMapping
    public ResponseEntity<String> atualizaAluno(@Valid @RequestBody AlunoDTO aluno) {
    	try {
    		service.update(aluno);
    	} catch (EntityNotFoundException e) {
			return ResponseEntity.notFound().build();
		}
    	return ResponseEntity.ok("Aluno is valid");
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deletaAluno(@PathVariable("id") Long id) {
		service.delete(id);
    	return ResponseEntity.ok("Aluno is deleted");
	}
    
    
    @ResponseStatus(HttpStatus.CONFLICT)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Map<String, String> handleValidationExceptions(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });
        return errors;
    }
}
