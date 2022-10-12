from django.contrib import admin

# Register your models here.
from task_manager.statuses.models import Status


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name', )


admin.site.register(Status, UserAdmin)
