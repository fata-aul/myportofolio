from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
import datetime

from main.forms import AcademicRecordForm, ExperienceForm
from main.models import AcademicRecord, Experience
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        

PROFILE = {
    "name": "Fata",
    "nama_lengkap": "Fata Akhmad Aulia",
    "npm": "2506540853",
    "study_program": "S1 Ilmu Komputer",
    "bio": "A Computer Science student thats hopefully graduate on time",
}


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Fata",
        "nama_lengkap": "Fata Akhmad Aulia",
        "npm": "2506540853",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A Computer Science student thats hopefully graduate on time"
        ),
        "last_login": last_login,
    }
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

@login_required(login_url="/login/") 
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = dict(PROFILE)
    context["form"] = form
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/") 
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")

    return redirect("main:show_experience")


def get_academic_json(request):
    institution_query = request.GET.get("institution", "").strip()
    academic_records = AcademicRecord.objects.all()

    if institution_query:
        academic_records = academic_records.filter(
            institution__icontains=institution_query
        )

    academic_json = serializers.serialize("json", academic_records)
    return HttpResponse(academic_json, content_type="application/json")


def show_academic(request):
    json_response = get_academic_json(request)

    academic_records = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    academic_records = [record.object for record in academic_records]

    context = dict(PROFILE)
    context["academic_list"] = academic_records
    context["institution_query"] = request.GET.get("institution", "").strip()
    return render(request, "academic.html", context)


@login_required(login_url="/login/") 
def create_academic(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = AcademicRecordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat akademik baru berhasil ditambahkan!")
        return redirect("main:show_academic")

    context = dict(PROFILE)
    context["form"] = form
    return render(request, "academic_form.html", context)


@login_required(login_url="/login/") 
def update_academic(request, academic_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    academic_record = get_object_or_404(AcademicRecord, pk=academic_id)
    form = AcademicRecordForm(request.POST or None, instance=academic_record)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat akademik berhasil diperbarui!")
        return redirect("main:show_academic")

    context = dict(PROFILE)
    context["form"] = form
    context["academic_record"] = academic_record
    return render(request, "academic_form.html", context)

@login_required(login_url="/login/") 
def delete_academic(request, academic_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    academic_record = get_object_or_404(AcademicRecord, pk=academic_id)

    if request.method == "POST":
        academic_record.delete()
        messages.success(request, "Riwayat akademik berhasil dihapus!")

    return redirect("main:show_academic")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


@login_required(login_url="/login/")
@login_required(login_url="/login/")
def toggle_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")