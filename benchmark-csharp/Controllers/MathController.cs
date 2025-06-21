using Microsoft.AspNetCore.Mvc;

namespace benchmark_csharp.Controllers;

[ApiController]
[Route("math")]
public class MathController : ControllerBase
{
    [HttpGet("fibonacci")]
    public IActionResult Fibonacci([FromQuery] int n = 30)
    {
        return Content(Fib(n).ToString(), "text/plain");
    }

    [HttpGet("fibonacci-iter")]
    public IActionResult FibonacciIter([FromQuery] int n = 30)
    {
        if (n <= 1) return Ok(n);
        long a = 0, b = 1;
        for (int i = 2; i <= n; i++)
        {
            long temp = a + b;
            a = b;
            b = temp;
        }
        return Content(b.ToString(), "text/plain");
    }

    [HttpGet("fibonacci/error")]
    public IActionResult FibonacciError([FromQuery] int n = 30)
    {
        return Content(FibWithError(n).ToString(), "text/plain");
    }

    [HttpPost("matrix/int")]
    public IActionResult MultiplyInt([FromBody] MatrixRequestInt request)
    {
        int[][] A = request.a;
        int[][] B = request.b;
        int n = A.Length, m = A[0].Length, k = B[0].Length;
        int[][] result = new int[n][];
        for (int i = 0; i < n; i++)
        {
            result[i] = new int[k];
            for (int j = 0; j < k; j++)
                for (int l = 0; l < m; l++)
                    result[i][j] += A[i][l] * B[l][j];
        }
        return Ok(result);
    }

    [HttpPost("matrix/float")]
    public IActionResult MultiplyFloat([FromBody] MatrixRequestFloat request)
    {
        double[][] A = request.a;
        double[][] B = request.b;
        int n = A.Length, m = A[0].Length, k = B[0].Length;
        double[][] result = new double[n][];
        for (int i = 0; i < n; i++)
        {
            result[i] = new double[k];
            for (int j = 0; j < k; j++)
                for (int l = 0; l < m; l++)
                    result[i][j] += A[i][l] * B[l][j];
        }
        return Ok(result);
    }

    private long Fib(int n)
    {
        if (n <= 1) return n;
        return Fib(n - 1) + Fib(n - 2);
    }

    private long FibWithError(int n)
    {
        if (n == 1)
            throw new Exception("Error while processing");
        if (n <= 0) return 0;
        return FibWithError(n - 1) + FibWithError(n - 2);
    }

    public class MatrixRequestInt
    {
        public int[][] a { get; set; }
        public int[][] b { get; set; }
    }

    public class MatrixRequestFloat
    {
        public double[][] a { get; set; }
        public double[][] b { get; set; }
    }
}
