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

    def test_academic_page_shows_data_when_not_empty(self):
        response = self.client.get(reverse("main:show_academic"))

        self.assertContains(response, self.record.institution)
        self.assertContains(response, self.record.description)
        self.assertContains(response, "Undergraduate")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_academic_page_shows_empty_message_when_empty(self):
        AcademicRecord.objects.all().delete()
        response = self.client.get(reverse("main:show_academic"))

        self.assertContains(response, "No academic record has been added yet.")

    def test_completed_academic_record(self):
        self.record.ended_at = timezone.now()
        self.record.save()
        response = self.client.get(reverse("main:show_academic"))

        self.assertFalse(self.record.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")