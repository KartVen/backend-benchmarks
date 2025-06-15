using Microsoft.AspNetCore.Mvc;

namespace benchmark_csharp.Controllers;


[ApiController]
[Route("/ping")]
public class HealthController : ControllerBase
{
    [HttpGet]
    public IActionResult Ping() => Ok("OK");
}