from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ExperienceForm
from main.models import AcademicRecord, Experience

PROFILE = {
    "name": "Fata",
    "nama_lengkap": "Fata Akhmad Aulia",
    "npm": "2506540853",
    "study_program": "S1 Ilmu Komputer",
    "bio": "A Computer Science student thats hopefully graduate on time",
}


def show_main(request):
    context = dict(PROFILE)
    return render(request, "index.html", context)


def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]

    groups = []
    group_by_label = {}
    for experience in experiences:
        label = experience.get_category_display()
        if label not in group_by_label:
            group_by_label[label] = {"label": label, "items": []}
            groups.append(group_by_label[label])
        group_by_label[label]["items"].append(experience)

    context = dict(PROFILE)
    context["experience_groups"] = groups
    context["title_query"] = request.GET.get("title", "").strip()
    return render(request, "experience.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = dict(PROFILE)
    context["form"] = form
    return render(request, "experience_form.html", context)


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")

    return redirect("main:show_experience")


def show_academic(request):
    context = dict(PROFILE)
    context["academic_list"] = AcademicRecord.objects.all()
    return render(request, "academic.html", context)