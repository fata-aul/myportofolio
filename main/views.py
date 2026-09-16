from django.shortcuts import render
from main.forms import ProjectForm

from main.models import AcademicRecord, Experience
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


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


def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Fata",
        "form": form,
    }
    return render(request, "projects_form.html", context)

from main.models import Project

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Burhan",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")
