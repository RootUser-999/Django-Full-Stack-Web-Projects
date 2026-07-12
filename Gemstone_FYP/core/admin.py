from django.contrib import admin
from .models import imageUpload


@admin.register(imageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ("id", "gem_image")
    list_display_links = ("id", "gem_image")
    search_fields = ("gem_image",)
    ordering = ("-id",)
    list_per_page = 20