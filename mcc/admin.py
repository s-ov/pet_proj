from django.contrib import admin
from .models import MotorControlCenter as MCC


@admin.register(MCC)
class MCCAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'substation',]
    list_display = ('title', 'slug', 'substation',)
    # prepopulated_fields = {"slug": ("title", )}
    list_display_links = ('title', )
    ordering = ['title']
