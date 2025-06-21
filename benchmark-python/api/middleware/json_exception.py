from django.http import JsonResponse
from datetime import datetime, timezone

class JsonExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        return JsonResponse({
            "message": str(exception) or "Internal server error",
            "status": 500,
            "exception": type(exception).__name__,
            "path": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }, status=500)