from django.urls import path
from . import views

urlpatterns = [
    path("ping", views.ping),
    path("math/fibonacci", views.fibonacci),
    path("persons", views.get_all_persons),
    path("persons/<int:id>", views.get_person),
    path("persons/<int:id>", views.update_person),
    path("persons/<int:id>", views.delete_person),
    path("persons", views.create_person),
]
