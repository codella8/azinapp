from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Work, Team, Contact

class WorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'url')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    
admin.site.register(Work, WorkAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "role")
    search_fields = ("name", "role")
admin.site.register(Team, TeamAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    
class ProfileInline(admin.StackedInline): # فیلد های مرتبط زیر هم نمایش داده شوند
    model = models.Profile
    can_delete = False

class CustomUserAdmin(BaseUserAdmin):
    #یعنی وقتی یک ادمین داره کاربری رو توی پنل جنگو می‌بینه یا ویرایش می‌کنه، پروفایل اون کاربر هم دقیقاً زیرش نمایش داده می‌شه.
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']

    
admin.site.register(Contact, ContactAdmin)