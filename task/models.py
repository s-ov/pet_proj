from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Task(models.Model):
    """The model describes servicing instance"""

    class TaskStatus(models.TextChoices):
        PENDING = 'PE', _('Призупинено')
        IN_PROGRESS = 'IP', _('На виконанні')
        COMPLETED = 'CO', _('Закінчено')
        CANCELED = 'CE', _('Скасовано')

    doer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    node = models.ForeignKey(
        'node.Node',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tasks'
    )
    task_description = models.TextField(default="Завдання не поставлено.")
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(
        blank=True, 
        null=True, 
    )
    status = models.CharField(
        max_length=2,
        choices=TaskStatus.choices,
        default=TaskStatus.IN_PROGRESS
    )

    class Meta:
        ordering = ['-created_at'] 
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return f'Завдання: {self.task_description}'
    

class UserTaskManager(models.Manager):
    def for_user(self, user):
        return self.filter(doer=user)
    

class UserTask(Task):
    objects = UserTaskManager()

    class Meta:
        proxy = True

    def __str__(self):
        return f"Task for {self.doer.first_name} - {self.task_description}"
