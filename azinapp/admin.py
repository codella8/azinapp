from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


# ======================================== #
# 1. PROFILE INLINE                       #
# ======================================== #

class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False
    verbose_name = "Profile"
    verbose_name_plural = "Profiles"


class CustomUserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']


# Unregister default User admin and register custom
try:
    admin.site.unregister(models.User)
except admin.sites.NotRegistered:
    pass
admin.site.register(models.User, CustomUserAdmin)


# ======================================== #
# 2. BASE ADMIN CLASSES                   #
# ======================================== #

class BaseProjectAdmin(admin.ModelAdmin):
    """کلاس پایه برای مدیریت پروژه‌ها با پیش‌نمایش تصویر"""
    list_display = ['image_preview', 'title', 'category', 'client', 'is_featured', 'is_published', 'sort_order']
    list_filter = ['category', 'is_featured', 'is_published']
    search_fields = ['title', 'description', 'client']
    list_editable = ['sort_order', 'is_featured', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['make_featured', 'make_unfeatured', 'publish_projects', 'unpublish_projects']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:6px;object-fit:cover;" />',
                obj.image.url
            )
        return format_html('<span style="color:#999;">No Image</span>')
    image_preview.short_description = "Preview"
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} item(s) marked as featured.")
    make_featured.short_description = "Mark selected as Featured"
    
    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} item(s) unmarked as featured.")
    make_unfeatured.short_description = "Unmark selected as Featured"
    
    def publish_projects(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} item(s) published.")
    publish_projects.short_description = "Publish selected items"
    
    def unpublish_projects(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} item(s) unpublished.")
    unpublish_projects.short_description = "Unpublish selected items"


class BaseImageInline(admin.TabularInline):
    extra = 3
    fields = ['image', 'caption', 'sort_order']
    classes = ['collapse']


# ======================================== #
# 3. TEAM ADMIN                           #
# ======================================== #

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['photo_preview', 'name', 'role']
    search_fields = ['name', 'role']
    list_filter = ['role']
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%;object-fit:cover;" />',
                obj.photo.url
            )
        return "No Photo"
    photo_preview.short_description = "Photo"


# ======================================== #
# 4. CONTACT ADMIN                        #
# ======================================== #

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_filter = ['created_at']
    readonly_fields = ['name', 'email', 'message', 'created_at']
    
    def has_add_permission(self, request):
        return False


# ======================================== #
# 6. MEDIA GALLERY ADMIN                  #
# ======================================== #

@admin.register(models.MediaGallery)
class MediaGalleryAdmin(admin.ModelAdmin):
    list_display = ['file_preview', 'title', 'category', 'is_video', 'is_featured', 'is_published', 'sort_order']
    list_filter = ['category', 'is_video', 'is_featured', 'is_published']
    search_fields = ['title', 'description']
    list_editable = ['sort_order', 'is_featured', 'is_published']
    
    def file_preview(self, obj):
        if obj.file:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:6px;object-fit:cover;" />',
                obj.file.url
            )
        return "No File"
    file_preview.short_description = "Preview"


# ======================================== #
# 7. GRAPHIC DESIGN ADMIN                 #
# ======================================== #

class GraphicProjectImageInline(BaseImageInline):
    model = models.GraphicProjectImage


@admin.register(models.GraphicDesignProject)
class GraphicDesignProjectAdmin(BaseProjectAdmin):
    model = models.GraphicDesignProject
    inlines = [GraphicProjectImageInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'category', 'client')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_published', 'sort_order')
        }),
    )


# ======================================== #
# 8. SMM ADMIN                            #
# ======================================== #

class SMMProjectImageInline(BaseImageInline):
    model = models.SMMProjectImage


@admin.register(models.SMMProject)
class SMMProjectAdmin(BaseProjectAdmin):
    model = models.SMMProject
    inlines = [SMMProjectImageInline]
    list_display = ['image_preview', 'title', 'category', 'platform', 'reach', 'engagement', 'is_featured', 'is_published', 'sort_order']
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'category', 'platform', 'client')
        }),
        ('Media', {
            'fields': ('image', 'is_video', 'video_url', 'video_file'),
            'classes': ('wide',)
        }),
        ('Statistics', {
            'fields': ('reach', 'engagement', 'likes', 'shares', 'comments'),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_published', 'sort_order')
        }),
    )


@admin.register(models.SMMProjectImage)
class SMMProjectImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'project', 'caption', 'sort_order']
    list_editable = ['sort_order']
    search_fields = ['caption', 'project__title']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:6px;object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"


@admin.register(models.SMMClient)
class SMMClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'is_active']
    list_filter = ['industry', 'is_active']
    search_fields = ['name', 'industry']
    list_editable = ['is_active']


# ======================================== #
# 9. WEB PROJECTS ADMIN                   #
# ======================================== #

class WebProjectImageInline(BaseImageInline):
    model = models.WebProjectImage


@admin.register(models.WebProject)
class WebProjectAdmin(BaseProjectAdmin):
    model = models.WebProject
    inlines = [WebProjectImageInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'category', 'client')
        }),
        ('Technical Details', {
            'fields': ('technologies', 'features', 'live_url')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_published', 'sort_order')
        }),
    )


# ======================================== #
# 10. MOBILE APP PROJECTS ADMIN           #
# ======================================== #

class MobileAppImageInline(BaseImageInline):
    model = models.MobileAppImage


@admin.register(models.MobileAppProject)
class MobileAppProjectAdmin(BaseProjectAdmin):
    model = models.MobileAppProject
    inlines = [MobileAppImageInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'category', 'client')
        }),
        ('Technical Details', {
            'fields': ('platform', 'technologies', 'features', 'app_store_url', 'play_store_url')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_published', 'sort_order')
        }),
    )


# ======================================== #
# 11. DATABASE PROJECTS ADMIN             #
# ======================================== #

class DatabaseProjectImageInline(BaseImageInline):
    model = models.DatabaseProjectImage


@admin.register(models.DatabaseProject)
class DatabaseProjectAdmin(BaseProjectAdmin):
    model = models.DatabaseProject
    inlines = [DatabaseProjectImageInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'category', 'client')
        }),
        ('Technical Details', {
            'fields': ('database_type', 'technologies', 'features')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_published', 'sort_order')
        }),
    )


# ======================================== #
# 12. SHOP PRODUCTS ADMIN                 #
# ======================================== #

class ShopProductImageInline(BaseImageInline):
    model = models.ShopProductImage


@admin.register(models.ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'title', 'category', 'is_published']
    list_filter = ['category','is_published']
    search_fields = ['title', 'description']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ShopProductImageInline]
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:6px;object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"


# ======================================== #
# 13. DECORE PROJECTS ADMIN               #
# ======================================== #

class DecoreProjectImageInline(BaseImageInline):
    model = models.DecoreProjectImage


@admin.register(models.DecoreProject)
class DecoreProjectAdmin(BaseProjectAdmin):
    model = models.DecoreProject
    inlines = [DecoreProjectImageInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'category', 'client', 'location', 'area')
        }),
        ('Design Details', {
            'fields': ('style', 'features')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_published', 'sort_order')
        }),
    )


# ======================================== #
# 15. ADMIN SITE HEADER & TITLE           #
# ======================================== #

admin.site.site_header = "AZIN GROUP Administration"
admin.site.site_title = "AZIN GROUP Admin"
admin.site.index_title = "Welcome to AZIN GROUP Management Dashboard"