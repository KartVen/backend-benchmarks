from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def ping(request):
    return HttpResponse("OK", content_type="text/plain")

def fibonacci(request):
    try:
        n = int(request.GET.get("n", 30))
    except (TypeError, ValueError):
        return HttpResponse("Invalid parameter", status=400, content_type="text/plain")

    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    return HttpResponse(str(fib(n)), content_type="text/plain")

@csrf_exempt
def create_person(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            person = Person.objects.create(name=data["name"], email=data["email"])
            return JsonResponse({"id": person.id, "name": person.name, "email": person.email}, status=201)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid input"}, status=400)

def get_all_persons(request):
    if request.method == "GET":
        persons = list(Person.objects.values("id", "name", "email"))
        return JsonResponse(persons, safe=False)

def get_person(request, id):
    if request.method == "GET":
        try:
            person = Person.objects.get(pk=id)
            return JsonResponse({"id": person.id, "name": person.name, "email": person.email})
        except Person.DoesNotExist:
            return HttpResponse(status=404)

@csrf_exempt
def update_person(request, id):
    if request.method == "PUT":
        try:
            person = Person.objects.get(pk=id)
            data = json.loads(request.body)
            person.name = data["name"]
            person.email = data["email"]
            person.save()
            return JsonResponse({"id": person.id, "name": person.name, "email": person.email})
        except Person.DoesNotExist:
            return HttpResponse(status=404)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid input"}, status=400)

@csrf_exempt
def delete_person(request, id):
    if request.method == "DELETE":
        try:
            person = Person.objects.get(pk=id)
            person.delete()
            return HttpResponse(status=204)
        except Person.DoesNotExist:
            return HttpResponse(status=404)