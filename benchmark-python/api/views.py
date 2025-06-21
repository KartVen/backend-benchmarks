from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


def ping(request):
    return HttpResponse("OK", content_type="text/plain")


def error(request):
    raise Exception("Simulated exception")


def fibonacci(request):
    n = int(request.GET.get("n", 30))

    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    return HttpResponse(str(fib(n)), content_type="text/plain")

def fibonacci_iter(request):
    n = int(request.GET.get("n", 30))
    if n <= 1:
        return HttpResponse(str(n))
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return HttpResponse(str(b), content_type="text/plain")

def fib(n):
    if n == 1:
        raise Exception("Error while processing")
    if n <= 0:
        return 0
    return fib(n - 1) + fib(n - 2)

def fibonacci_error(request):
    n = int(request.GET.get("n", 30))
    return HttpResponse(str(fib(n)), content_type="text/plain")

@csrf_exempt
def multiply_matrices_int(request):
    data = json.loads(request.body)
    A = data["a"]
    B = data["b"]
    n, m, k = len(A), len(A[0]), len(B[0])
    result = [[0] * k for _ in range(n)]
    for i in range(n):
        for j in range(k):
            for l in range(m):
                result[i][j] += A[i][l] * B[l][j]
    return JsonResponse(result, safe=False)


@csrf_exempt
def multiply_matrices_float(request):
    data = json.loads(request.body)
    A = data["a"]
    B = data["b"]
    n, m, k = len(A), len(A[0]), len(B[0])
    result = [[0.0] * k for _ in range(n)]
    for i in range(n):
        for j in range(k):
            for l in range(m):
                result[i][j] += A[i][l] * B[l][j]
    return JsonResponse(result, safe=False)


@csrf_exempt
def upload_json(request):
    if request.method != "POST":
        return HttpResponse(status=405)
    gmail_count = sum(1 for p in json.loads(request.body) if "email" in p and "gmail.com" in p["email"])
    return JsonResponse({
        "gmailCount": gmail_count
    })
