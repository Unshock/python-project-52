# Generated by Django 4.1.1 on 2022-10-22 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("labels", "0002_remove_label_tasks_alter_label_creator"),
        ("tasks", "0008_alter_taskslabels_options_alter_task_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskslabels",
            name="label",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="labels.label",
            ),
        ),
        migrations.AlterField(
            model_name="taskslabels",
            name="task",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="tasks.task"
            ),
        ),
    ]
