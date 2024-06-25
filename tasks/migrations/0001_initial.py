# Generated by Django 4.2.5 on 2024-06-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "taskname",
                    models.CharField(max_length=50, unique=True, verbose_name="Задача"),
                ),
                (
                    "taskdescription",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                ("taskautor", models.CharField(max_length=50, verbose_name="Автор")),
                (
                    "time_create",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
            ],
            options={
                "verbose_name": "Задачи",
                "verbose_name_plural": "Задачи",
                "ordering": ["taskname"],
            },
        ),
    ]
