from django.contrib import admin
from .models import *


class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )#'tasks')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name', )


admin.site.register(Label, LabelAdmin)
