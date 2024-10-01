from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from node.models import Node


def get_default_node():
    return "Вузол для обслуговування не вказано."


class Task(models.Model):
    """The model describes servicing instance"""
    
    created_at = models.DateTimeField(auto_now_add=True)
    deadline =models.DateTimeField(blank=True, null=True, help_text="Дата та час до якого завдання має бути викононе.")

    class TaskStatus(models.TextChoices):
        PENDING = 'PE', _('Pending')
        IN_PROGRESS = 'IP', _('In Progress')
        COMPLETED = 'CO', _('Completed')

    doer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    node = models.ForeignKey(
        Node,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tasks'
    )
    task_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text=_("Deadline for the task to be completed.")
    )
    status = models.CharField(
        max_length=2,
        choices=TaskStatus.choices,
        default=TaskStatus.IN_PROGRESS
    )

    class Meta:
        ordering = ['created_at'] 
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return f'Завдання: {self.task_description[:20]} - для {self.doer}'
