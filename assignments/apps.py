from django.apps import AppConfig


class AssignmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assignments'

    def ready(self):
        """Import and register the signal handlers"""
        
        import assignments.signals
