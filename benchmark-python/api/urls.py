from django.urls import path
from . import views

urlpatterns = [
    path("ping", views.ping),
    path("error", views.error),
    path("math/fibonacci", views.fibonacci),
    path("math/fibonacci-iter", views.fibonacci_iter),
    path("math/fibonacci/error", views.fibonacci_error),
    path("math/matrix/int", views.multiply_matrices_int),
    path("math/matrix/float", views.multiply_matrices_float),
    path("upload-json", views.upload_json),
]
