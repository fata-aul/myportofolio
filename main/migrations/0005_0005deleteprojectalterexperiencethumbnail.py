from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_project"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Project",
        ),
        migrations.AlterField(
            model_name="experience",
            name="thumbnail",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]