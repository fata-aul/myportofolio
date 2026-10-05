from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
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
from django.utils.formats import date_format
from django.views.decorators.http import require_POST

PROFILE = {
    "name": "Fata",
    "nama_lengkap": "Fata Akhmad Aulia",
    "npm": "2506540853",
    "study_program": "S1 Ilmu Komputer",
    "bio": "A Computer Science student thats hopefully graduate on time",
}

def require_editor(user):
    if not (user.is_superuser or user.groups.filter(name ="Editor").exists()):
        raise PermissionDenied
    


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
    experiences = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for experience in experiences:
        starred_users = list(experience.starred_by.all())  
        is_starred = (
            request.user in starred_users if request.user.is_authenticated else False
        )
        data.append(
            {
                "pk": str(experience.id),
                "fields": {
                    "title": experience.title,
                    "organization": experience.organization,
                    "description": experience.description,
                    "category": experience.category,
                    "category_label": experience.get_category_display(),
                    "thumbnail": experience.thumbnail or "",
                    "started_label": date_format(experience.started_at, "M Y"),
                    "ended_label": (
                        date_format(experience.ended_at, "M Y")
                        if experience.ended_at
                        else "Sekarang"
                    ),
                    "is_ongoing": experience.is_ongoing,
                    "star_count": len(starred_users),
                    "is_starred": is_starred,
                    "starred_by_names": ", ".join(u.username for u in starred_users),
                },
            }
        )

    return JsonResponse(data, safe=False)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fata",
        "title_query": title_query,
    }
    context["form"] = ExperienceForm()
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

@login_required(login_url="/login/") 
def update_experience(request, experience_id):
    require_editor(request.user)
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = dict(PROFILE)
    context["form"] = form
    context["experience"] = experience
    return render(request, "experience_form.html", context)


def get_academic_json(request):
    institution_query = request.GET.get("institution", "").strip()
    academic_records = AcademicRecord.objects.all()

    if institution_query:
        academic_records = academic_records.filter(
            institution__icontains=institution_query
        )

    # JSON dirakit manual dengan JsonResponse
    data = []
    for record in academic_records:
        data.append(
            {
                "pk": str(record.id),
                "fields": {
                    "level": record.level,
                    "level_label": record.get_level_display(),
                    "institution": record.institution,
                    "description": record.description,
                    "logo": record.logo or "",
                    "started_year": record.started_at.year,
                    "ended_year": record.ended_at.year if record.ended_at else None,
                    "is_ongoing": record.is_ongoing,
                },
            }
        )

    return JsonResponse(data, safe=False)


def show_academic(request):
    # Halaman hanya merender kerangka; datanya diambil JS lewat get_academic_json
    is_editor = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Editor").exists()
    )

    context = dict(PROFILE)
    context["institution_query"] = request.GET.get("institution", "").strip()
    context["form"] = AcademicRecordForm()
    context["is_editor"] = is_editor
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
    require_editor(request.user)
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
def toggle_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@require_POST
def create_experience_ajax(request):
 
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pengalaman."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@require_POST
def create_academic_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan riwayat akademik."},
            status=403,
        )

    form = AcademicRecordForm(request.POST)
    if form.is_valid():
        record = form.save()
        return JsonResponse(
            {"message": "Riwayat akademik berhasil ditambahkan.", "pk": str(record.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)