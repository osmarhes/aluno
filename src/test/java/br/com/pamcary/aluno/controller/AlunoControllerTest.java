package br.com.pamcary.aluno.controller;

import br.com.pamcary.aluno.AlunoApplication;
import br.com.pamcary.aluno.model.Aluno;
import br.com.pamcary.aluno.repository.AlunoRepository;
import br.com.pamcary.aluno.view.AlunoDTO;
import org.junit.Assert;
import org.junit.FixMethodOrder;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.MethodSorters;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import java.io.IOException;
import java.util.Collections;

import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.collection.IsCollectionWithSize.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT, classes = AlunoApplication.class)
//@WebMvcTest(AlunoController.class)
@AutoConfigureTestDatabase
@AutoConfigureMockMvc
@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class AlunoControllerTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private AlunoRepository alunoService;

    @Test
    public void test1Post() throws Exception {
        AlunoDTO alunoDTO = new AlunoDTO();
        alunoDTO.setIdade(10);
        alunoDTO.setNome("Aline");

        mvc.perform(post("/aluno")
                .contentType(MediaType.APPLICATION_JSON).content(JsonUtil.toJson(alunoDTO)))
                .andDo(print())
                .andExpect(status().isOk());

        mvc.perform(get("/aluno")
                .contentType(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].nome", is("Aline")))
                .andExpect(jsonPath("$[0].idade", is(10)));
    }

    @Test
    public void test2Put() throws Exception {
        Aluno aluno = new Aluno();
        aluno.setIdade(10);
        aluno.setNome("Clara");

        alunoService.save(aluno);

        AlunoDTO alunoDTO = new AlunoDTO();
        alunoDTO.setId(aluno.getId());
        alunoDTO.setIdade(12);
        alunoDTO.setNome("Clara Put");

        mvc.perform(put("/aluno")
                .contentType(MediaType.APPLICATION_JSON).content(JsonUtil.toJson(alunoDTO)))
                .andDo(print())
                .andExpect(status().isOk());

        mvc.perform(get("/aluno")
                .contentType(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[1].nome", is("Clara Put")))
                .andExpect(jsonPath("$[1].idade", is(12)));
    }

    @Test
    public void test3Delete() throws Exception {
        Aluno aluno = new Aluno();
        aluno.setIdade(10);
        aluno.setNome("Jorge");

        alunoService.save(aluno);

        mvc.perform(delete("/aluno/" + aluno.getId())
                .contentType(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk());

        Assert.assertFalse(alunoService.existsById(aluno.getId()));
    }
    @Test
    public void teste4GetAll() throws Exception {
        mvc.perform(get("/aluno")
            .contentType(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].nome", is("Aline")))
                .andExpect(jsonPath("$[0].idade", is(10)))
                .andExpect(jsonPath("$[1].nome", is("Clara Put")))
                .andExpect(jsonPath("$[1].idade", is(12)))
                .andExpect(jsonPath("$.*", hasSize(2)));

    }

    @Test
    public void teste5CamposRequeridos() throws Exception {
        AlunoDTO alunoDTO = new AlunoDTO();
        alunoDTO.setNome("Aline");

        mvc.perform(post("/aluno")
                .contentType(MediaType.APPLICATION_JSON).content(JsonUtil.toJson(alunoDTO)))
                .andDo(print())
                .andExpect(status().isConflict());

        alunoDTO.setNome("");
        alunoDTO.setIdade(10);

        mvc.perform(post("/aluno")
                .contentType(MediaType.APPLICATION_JSON).content(JsonUtil.toJson(alunoDTO)))
                .andDo(print())
                .andExpect(status().isConflict());


    }

    @Test
    public void test6NotFoundEntity() throws Exception {
        AlunoDTO alunoDTO = new AlunoDTO();
        alunoDTO.setId(20l);
        alunoDTO.setIdade(10);
        alunoDTO.setNome("Aline");

        mvc.perform(put("/aluno")
                .contentType(MediaType.APPLICATION_JSON).content(JsonUtil.toJson(alunoDTO)))
                .andDo(print())
                .andExpect(status().isNotFound());
    }
}
