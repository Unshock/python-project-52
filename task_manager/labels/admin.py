from django.contrib import admin
from task_manager.labels.models import Label
from ..tasks.admin import TasksLabelsInline


class LabelAdmin(admin.ModelAdmin):
    inlines = (TasksLabelsInline,)
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name', )


admin.site.register(Label, LabelAdmin)
