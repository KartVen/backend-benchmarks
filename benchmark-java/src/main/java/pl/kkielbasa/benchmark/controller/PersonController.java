package pl.kkielbasa.benchmark.controller;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pl.kkielbasa.benchmark.repository.PersonRepository;

import java.util.List;
import java.util.Map;

@RestController
public class PersonController {

    @PostMapping("/upload-json")
    public Map<String, Object> uploadJson(@RequestBody List<PersonRequest> persons) {
        var gmailCount = persons.stream().filter(p -> p.getEmail() != null && p.getEmail().contains("gmail.com")).count();
        return Map.of("gmailCount", gmailCount);
    }

    @Data
    public static class PersonRequest {
        private String name;
        private String email;
    }
}