using benchmark_csharp.Models;
using Microsoft.EntityFrameworkCore;

namespace benchmark_csharp.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Person> Persons { get; set; }
}