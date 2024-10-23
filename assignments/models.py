from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class TaskAssignment(models.Model):
    """
    Mediator model that links an Employee to a Task, allowing for more flexibility and additional metadata
    about the assignment itself.
    """

    doer = models.ForeignKey(
        'users.Employee',
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_('Співробітник'),
    )
    task = models.ForeignKey(
        'task.Task',
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_('Завдання')
    )
    node = models.ForeignKey(
        'node.Node', 
        on_delete=models.CASCADE,
        blank=True, null=True, 
        verbose_name=_('Вузол'))

    class Meta:
        verbose_name = _('Завдання працівника')
        verbose_name_plural = _('Завдання працівника')
        unique_together = ('doer', 'task')

    # def __str__(self):
    #     return f'{self.employee} - {self.task} ({self.get_status_display()})'

