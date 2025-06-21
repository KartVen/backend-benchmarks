package pl.kkielbasa.benchmark.controller;

import lombok.Getter;
import lombok.Setter;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/math")
public class MathController {

    @GetMapping("/fibonacci")
    public long fibonacci(@RequestParam(defaultValue = "30") int n) {
        return fib(n);
    }

    @GetMapping("/fibonacci-iter")
    public long fibonacciIter(@RequestParam(defaultValue = "30") int n) {
        if (n <= 1) return n;
        long a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            long temp = a + b;
            a = b;
            b = temp;
        }
        return b;
    }

    @GetMapping("/fibonacci/error")
    public long fibonacciError(@RequestParam(defaultValue = "30") int n) {
        return fibWithError(n);
    }

    private long fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }

    private long fibWithError(int n) {
        if (n == 1) throw new RuntimeException("Error while processing");
        if (n <= 0) return 0;
        return fibWithError(n - 1) + fibWithError(n - 2);
    }

    @PostMapping("/matrix/int")
    public int[][] multiplyInt(@RequestBody MatrixRequestInt request) {
        int[][] A = request.getA();
        int[][] B = request.getB();
        int n = A.length, m = A[0].length, k = B[0].length;
        int[][] result = new int[n][k];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < k; j++)
                for (int l = 0; l < m; l++)
                    result[i][j] += A[i][l] * B[l][j];
        return result;
    }

    @PostMapping("/matrix/float")
    public double[][] multiplyFloat(@RequestBody MatrixRequestFloat request) {
        double[][] A = request.getA();
        double[][] B = request.getB();
        int n = A.length, m = A[0].length, k = B[0].length;
        double[][] result = new double[n][k];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < k; j++)
                for (int l = 0; l < m; l++)
                    result[i][j] += A[i][l] * B[l][j];
        return result;
    }

    @Getter
    @Setter
    public static class MatrixRequestInt {
        private int[][] a;
        private int[][] b;
    }

    @Getter
    @Setter
    public static class MatrixRequestFloat {
        private double[][] a;
        private double[][] b;
    }
}