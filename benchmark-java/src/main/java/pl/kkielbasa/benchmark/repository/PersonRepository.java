package pl.kkielbasa.benchmark.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.kkielbasa.benchmark.model.Person;

public interface PersonRepository extends JpaRepository<Person, Long> {
}