from django.shortcuts import render

from main.models import AcademicRecord, Experience


def show_main(request):
    context = {
        "name": "Fata",
        "nama_lengkap" : "Fata Akhmad Aulia",
        "npm": "2506540853",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A Computer Science student thats hopefully graduate on time"
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fata",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_academic(request):
    context = {
        "name": "Fata",
        "academic_list": AcademicRecord.objects.all(),
    }
    return render(request, "academic.html", context)