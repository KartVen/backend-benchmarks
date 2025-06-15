using benchmark_csharp.Data;
using benchmark_csharp.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace benchmark_csharp.Controllers;

[ApiController]
[Route("persons")]
public class PersonsController(AppDbContext context) : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> Create(Person person)
    {
        context.Persons.Add(person);
        await context.SaveChangesAsync();
        return CreatedAtAction(nameof(GetById), new { id = person.Id }, person);
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<Person>>> GetAll()
    {
        return await context.Persons.ToListAsync();
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Person>> GetById(long id)
    {
        var person = await context.Persons.FindAsync(id);
        return person == null ? NotFound() : Ok(person);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Put(long id, Person updated)
    {
        var person = await context.Persons.FindAsync(id);
        if (person == null) return NotFound();

        person.Name = updated.Name;
        person.Email = updated.Email;

        await context.SaveChangesAsync();
        return Ok(person);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(long id)
    {
        var person = await context.Persons.FindAsync(id);
        if (person == null) return NotFound();

        context.Persons.Remove(person);
        await context.SaveChangesAsync();
        return NoContent();
    }
}