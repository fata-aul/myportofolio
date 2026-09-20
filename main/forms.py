from django.forms import DateInput, ModelForm, Select, Textarea, TextInput, URLInput

from main.models import Experience


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "organization",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "organization": "Organisasi / Perusahaan",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori",
            "thumbnail": "URL Gambar",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai (kosongkan jika masih berjalan)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Backend Developer Intern",
                    "maxlength": 255,
                }
            ),
            "organization": TextInput(
                attrs={
                    "placeholder": "Fakultas Ilmu Komputer UI",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan apa yang kamu kerjakan di sini",
                    "rows": 3,
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "started_at": DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
            "ended_at": DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
        }