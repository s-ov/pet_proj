from django.db.models.signals import post_save
from django.dispatch import receiver
from task.models import Task
from .models import TaskAssignment

@receiver(post_save, sender=Task)
def create_task_assignment(sender, instance, created, **kwargs):
    """
    Signal that triggers after a Task is created to automatically
    create a corresponding TaskAssignment entry.
    
    Args:
        sender: The model class (Task).
        instance: The actual instance being saved (the Task instance).
        created: Boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        if instance.doer and instance.node:
            TaskAssignment.objects.create(
                doer=instance.doer,
                task=instance,
                node=instance.node
            )
        else:
            print("Task does not have a doer or node, TaskAssignment not created.")
