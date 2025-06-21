package pl.kkielbasa.benchmark.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.kkielbasa.benchmark.model.Person;

import java.util.List;

public interface PersonRepository extends JpaRepository<Person, Long> {
    List<Person> findTop10ByOrderByNameAsc();
}