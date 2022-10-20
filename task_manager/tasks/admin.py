from django.contrib import admin
from .models import *


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'executor',)# 'status')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name', )


admin.site.register(Task, TaskAdmin)
