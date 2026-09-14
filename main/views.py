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
    experiences = Experience.objects.all()

    groups = []
    group_by_label = {}
    for experience in experiences:
        label = experience.get_category_display()
        if label not in group_by_label:
            group_by_label[label] = {"label": label, "items": []}
            groups.append(group_by_label[label])
        group_by_label[label]["items"].append(experience)

    context = {
        "name": "Fata",
        "experience_groups": groups,
    }
    return render(request, "experience.html", context)


def show_academic(request):
    context = {
        "name": "Fata",
        "academic_list": AcademicRecord.objects.all(),
    }
    return render(request, "academic.html", context)