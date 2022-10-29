from django.contrib import admin
from task_manager.tasks.models import Task, TasksLabels


class TasksLabelsInline(admin.TabularInline):
    model = TasksLabels
    extra = 1
    # list_display = ('id', 'task', 'label')
    # list_display_links = ('id', 'task', 'label')


class TaskAdmin(admin.ModelAdmin):
    inlines = (TasksLabelsInline,)
    list_display = ('id', 'name', 'description', 'executor')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name', )


class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'task')
    list_display_links = ('id', 'task')


class LabelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'label')
    list_display_links = ('id', 'label')


admin.site.register(Task, TaskAdmin)
