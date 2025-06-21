using benchmark_csharp.Models;
using Microsoft.AspNetCore.Mvc;

namespace benchmark_csharp.Controllers;

[ApiController]
[Route("")]
public class PersonsController : ControllerBase
{
    [HttpPost("upload-json")]
    public IActionResult UploadJson([FromBody] List<PersonRequest> persons)
    {
        var gmailCount = persons.Count(p => p.Email != null && p.Email.Contains("gmail.com"));
        return Ok(new
        {
            gmailCount
        });
    }

    public class PersonRequest
    {
        public string? Name { get; set; }
        public string? Email { get; set; }
    }
}
