from django.contrib import admin

from .models import WorkTowerLevel


@admin.register(WorkTowerLevel)
class WorkTowerLevelAdmin(admin.ModelAdmin):
    list_display = ('level',)
