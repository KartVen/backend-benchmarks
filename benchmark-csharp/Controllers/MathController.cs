using Microsoft.AspNetCore.Mvc;

namespace benchmark_csharp.Controllers;


[ApiController]
[Route("math")]
public class MathController : ControllerBase
{
    [HttpGet("fibonacci")]
    public IActionResult Fibonacci([FromQuery] int n = 30)
    {
        return Ok(Fib(n));
    }

    private long Fib(int n)
    {
        if (n <= 1) return n;
        return Fib(n - 1) + Fib(n - 2);
    }
}