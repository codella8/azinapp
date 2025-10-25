from django.contrib import admin
from . import models
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
    
admin.site.register(Contact, ContactAdmin)