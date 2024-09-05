from django.contrib import admin

from .models import Node, NodeMotor


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'index', 'level', 'motor', 'mcc')

@admin.register(NodeMotor)
class NodeMotorAdmin(admin.ModelAdmin):
    list_display = ('power', 'round_per_minute', 'connection', 'amperage')
