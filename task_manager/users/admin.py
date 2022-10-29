from django.contrib import admin

from task_manager.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')
    list_display_links = ('id', 'username')
    search_fields = ('username',)
    list_filter = ('username', )


admin.site.register(User, UserAdmin)
