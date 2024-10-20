from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from task.models import Task
from users.models import Employee


class EmployeeTaskAssignment(models.Model):
    """
    Mediator model that links an Employee to a Task, allowing for more flexibility and additional metadata
    about the assignment itself.
    """
    
    class AssignmentStatus(models.TextChoices):
        ASSIGNED = 'AS', _('Призначено')
        ACCEPTED = 'AC', _('Прийнято')
        REJECTED = 'RE', _('Відхилено')
        COMPLETED = 'CO', _('Виконано')

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_('Employee')
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_('Task')
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.ASSIGNED
    )
    notes = models.TextField(blank=True, null=True, verbose_name=_('Assignment Notes'))

    class Meta:
        verbose_name = _('Employee Task Assignment')
        verbose_name_plural = _('Employee Task Assignments')
        unique_together = ('employee', 'task')

    def __str__(self):
        return f'{self.employee} - {self.task} ({self.get_status_display()})'

