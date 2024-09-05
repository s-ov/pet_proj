from typing import Dict, Tuple
from django.contrib import admin

from .models import Substation


@admin.register(Substation)
class SubstationAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'level',)
    prepopulated_fields = {"slug": ("title", )}

    # def get_prepopulated_fields(self, request, obj=None) -> Dict[str, Tuple[str]]:
    #     """
    #         Pre-populate field 'slug' with the content of field 'title'
    #     """
    #     return {
    #         'slug': ('title',),
    #     }
