# Generated by Django 4.1.2 on 2022-11-08 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="status",
            name="creator",
        ),
    ]
