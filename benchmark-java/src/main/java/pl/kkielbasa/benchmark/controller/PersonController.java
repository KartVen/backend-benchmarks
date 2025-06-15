package pl.kkielbasa.benchmark.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pl.kkielbasa.benchmark.model.Person;
import pl.kkielbasa.benchmark.repository.PersonRepository;

import java.util.List;

@RestController
@RequestMapping("/persons")
public class PersonController {

    private final PersonRepository personRepo;

    public PersonController(PersonRepository personRepo) {
        this.personRepo = personRepo;
    }

    @PostMapping
    public Person create(@RequestBody Person person) {
        return personRepo.save(person);
    }

    @GetMapping
    public List<Person> getAll() {
        return personRepo.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Person> get(@PathVariable Long id) {
        return personRepo.findById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}")
    public Person put(@PathVariable Long id, @RequestBody Person updated) {
        Person person = personRepo.findById(id).orElseThrow();
        person.setName(updated.getName());
        person.setEmail(updated.getEmail());
        return personRepo.save(person);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        personRepo.deleteById(id);
    }
}