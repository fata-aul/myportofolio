from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import AcademicRecord, Experience


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")


class AcademicTest(TestCase):
    def setUp(self):
        self.record = AcademicRecord.objects.create(
            level="undergraduate",
            institution="Universitas Indonesia",
            description="S1 Ilmu Komputer",
            started_at="2025-08-01",
        )

    def test_academic_url_is_accessible(self):
        response = self.client.get(reverse("main:show_academic"))

        self.assertEqual(response.status_code, 200)

    def test_academic_url_uses_correct_template(self):
        response = self.client.get(reverse("main:show_academic"))

        self.assertTemplateUsed(response, "academic.html")

    def test_academic_model(self):
        self.assertEqual(
            str(self.record), "Undergraduate - Universitas Indonesia"
        )
        self.assertEqual(self.record.level, "undergraduate")
        self.assertTrue(self.record.is_ongoing)

    def test_academic_page_renders_skeleton_only(self):
        response = self.client.get(reverse("main:show_academic"))

        # Data tidak lagi dirender server; diambil JS lewat endpoint JSON
        self.assertNotContains(response, self.record.institution)
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, reverse("main:get_academic_json"))
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_academic_json_returns_data(self):
        response = self.client.get(reverse("main:get_academic_json"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        fields = data[0]["fields"]
        self.assertEqual(data[0]["pk"], str(self.record.id))
        self.assertEqual(fields["institution"], "Universitas Indonesia")
        self.assertEqual(fields["level_label"], "Undergraduate")
        self.assertTrue(fields["is_ongoing"])
        self.assertIsNone(fields["ended_year"])

    def test_academic_json_search(self):
        found = self.client.get(
            reverse("main:get_academic_json"), {"institution": "indonesia"}
        )
        missing = self.client.get(
            reverse("main:get_academic_json"), {"institution": "xyz"}
        )

        self.assertEqual(len(found.json()), 1)
        self.assertEqual(missing.json(), [])

    def test_academic_json_completed_record(self):
        self.record.ended_at = timezone.now()
        self.record.save()
        fields = self.client.get(reverse("main:get_academic_json")).json()[0]["fields"]

        self.assertFalse(fields["is_ongoing"])
        self.assertEqual(fields["ended_year"], timezone.now().year)


class AcademicAjaxCreateTest(TestCase):
    payload = {
        "level": "undergraduate",
        "institution": "Universitas Indonesia",
        "description": "S1 Ilmu Komputer",
        "logo": "",
        "started_at": "2025-08-01",
        "ended_at": "",
    }

    def setUp(self):
        self.url = reverse("main:create_academic_ajax")
        self.superuser = User.objects.create_superuser("owner", password="pass12345")
        self.regular = User.objects.create_user("visitor", password="pass12345")

    def test_anonymous_gets_403_json(self):
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertIn("message", response.json())
        self.assertEqual(AcademicRecord.objects.count(), 0)

    def test_regular_user_gets_403_json(self):
        self.client.login(username="visitor", password="pass12345")
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(AcademicRecord.objects.count(), 0)

    def test_get_not_allowed(self):
        self.client.login(username="owner", password="pass12345")

        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_superuser_creates_record_201(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(AcademicRecord.objects.count(), 1)

    def test_invalid_input_gets_400_with_errors(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(self.url, {**self.payload, "institution": ""})

        self.assertEqual(response.status_code, 400)
        self.assertIn("institution", response.json()["errors"])
        self.assertEqual(AcademicRecord.objects.count(), 0)

    def test_html_only_institution_is_rejected(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(
            self.url,
            {**self.payload, "institution": "<img src=x onerror=alert(1)>"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(AcademicRecord.objects.count(), 0)

    def test_html_tags_are_stripped_from_description(self):
        self.client.login(username="owner", password="pass12345")
        self.client.post(self.url, {**self.payload, "description": "Halo <b>dunia</b>"})

        self.assertEqual(AcademicRecord.objects.get().description, "Halo dunia")