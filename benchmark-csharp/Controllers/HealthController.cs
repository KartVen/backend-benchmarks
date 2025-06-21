using Microsoft.AspNetCore.Mvc;

namespace benchmark_csharp.Controllers;

[ApiController]
[Route("")]
public class HealthController : ControllerBase
{
    [HttpGet("ping")]
    public IActionResult Ping() => Content("OK", "text/plain");

    [HttpGet("error")]
    public IActionResult Error() => throw new Exception("Simulated exception");
}
