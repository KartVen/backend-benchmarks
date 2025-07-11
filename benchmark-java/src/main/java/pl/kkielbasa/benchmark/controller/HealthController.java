package pl.kkielbasa.benchmark.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

    @GetMapping("/ping")
    public String ping() {
        return "OK";
    }

    @GetMapping("/error")
    public String error() {
        throw new RuntimeException("Simulated exception");
    }
}