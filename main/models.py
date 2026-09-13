import uuid

from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class AcademicRecord(models.Model):
    LEVEL_CHOICES = [
        ("junior-high", "Junior High School"),
        ("senior-high", "Senior High School"),
        ("undergraduate", "Undergraduate"),
        ("graduate", "Graduate"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="undergraduate",
    )
    institution = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    started_at = models.DateField()
    ended_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["started_at"]

    def __str__(self):
        return f"{self.get_level_display()} - {self.institution}"

    @property
    def is_ongoing(self):
        return self.ended_at is None