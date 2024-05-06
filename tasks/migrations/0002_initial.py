# Generated by Django 4.2.5 on 2024-04-24 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("statuses", "0001_initial"),
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="executor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Исполнитель",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="statuses.status",
                verbose_name="Статус",
            ),
        ),
    ]
