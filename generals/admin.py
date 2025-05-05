from django.contrib import admin

from .models import Catalogue, CatalogueImage


@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(CatalogueImage)
class CatalogueImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'catalogue']