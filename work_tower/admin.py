from django.contrib import admin

from .models import WorkTowerLevel


@admin.register(WorkTowerLevel)
class WorkTowerAreasAdmin(admin.ModelAdmin):
    list_display = ('level',)
