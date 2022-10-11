from django.contrib import admin

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')
    list_display_links = ('id', 'username')
    search_fields = ('username',)
    list_filter = ('username', )


admin.site.register(User, UserAdmin)
