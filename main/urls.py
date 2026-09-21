from django.urls import path

from main.views import (
    create_academic,
    create_experience,
    delete_academic,
    delete_experience,
    get_academic_json,
    get_experiences_json,
    show_academic,
    show_experience,
    show_main,
    update_academic,
    register,
    login_user,
    logout_user,
    toggle_star,
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
    path("academic/add/", create_academic, name="create_academic"),
    path(
        "academic/<uuid:academic_id>/edit/",
        update_academic,
        name="update_academic",
    ),
    path(
        "academic/<uuid:academic_id>/delete/",
        delete_academic,
        name="delete_academic",
    ),
    path("api/academic/", get_academic_json, name="get_academic_json"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path(
    "experience/<uuid:experience_id>/star/",
    toggle_star,
    name="toggle_star",
    ),
]