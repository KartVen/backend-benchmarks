package pl.kkielbasa.benchmark.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletRequest;
import java.time.LocalDateTime;
import java.util.Map;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    @ResponseBody
    public ResponseEntity<?> handleException(Exception ex, HttpServletRequest request) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(
            Map.of(
                "message", ex.getMessage(),
                "status", 500,
                "exception", ex.getClass().getSimpleName(),
                "path", request.getRequestURI(),
                "timestamp", LocalDateTime.now().toString()
            )
        );
    }

    @ExceptionHandler(StackOverflowError.class)
    @ResponseBody
    public ResponseEntity<?> handleStackOverflowError(StackOverflowError err, HttpServletRequest request) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(
            Map.of(
                "message", "Stack overflow: recursion too deep",
                "status", 500,
                "exception", err.getClass().getSimpleName(),
                "path", request.getRequestURI(),
                "timestamp", LocalDateTime.now().toString()
            )
        );
    }
}