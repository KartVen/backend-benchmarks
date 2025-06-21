using System.Text.Json;

namespace benchmark_csharp.Middleware;

public class GlobalExceptionMiddleware
{
    private readonly RequestDelegate _next;

    public GlobalExceptionMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task Invoke(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            await HandleExceptionAsync(context, ex);
        }
    }

    private static Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        context.Response.StatusCode = 500;
        context.Response.ContentType = "application/json";

        var result = JsonSerializer.Serialize(new
        {
            status = 500,
            message = "Internal Server Error",
            exception = exception.GetType().Name,
            timestamp = DateTime.UtcNow,
            path = context.Request.Path.Value
        });

        return context.Response.WriteAsync(result);
    }
}