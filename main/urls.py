from django.urls import path

from main.views import (
    create_experience,
    delete_experience,
    get_experiences_json,
    show_academic,
    show_experience,
    show_main,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path(
        "experience/<uuid:experience_id>/delete/",
        delete_experience,
        name="delete_experience",
    ),
    path("api/experience/", get_experiences_json, name="get_experiences_json"),
    path("academic/", show_academic, name="show_academic"),
]