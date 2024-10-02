from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class MotorControlCenter(models.Model):
    """
        The model represents MCC(Motor Control Centers) on the work tower
    """
    MCC_NAMES = [
        ('MCC-1', 'Motor Control Center 1'),
        ('MCC-2', 'Motor Control Center 2'),
        ('MCC-3', 'Motor Control Center 3'),
        ('MCC-4', 'Motor Control Center 4'),
        ('MCC-5', 'Motor Control Center 5'),
        ('MCC-6', 'Motor Control Center 6'),
        ('MCC-7', 'Motor Control Center 7'),
        ('MCC-8', 'Motor Control Center 8'),
        ('MCC-9', 'Motor Control Center 9'),
        ('MCC-10', 'Motor Control Center 10'),
        ('MCC-11', 'Motor Control Center 11'),
    ]
    title = models.CharField(max_length=10, choices=MCC_NAMES)
    slug = models.SlugField(unique=True, db_index=True, blank=True)
    substation = models.ForeignKey('substation.Substation', 
                                    on_delete=models.PROTECT,
                                    related_name='mccs',
                                    blank=True, null=True)
    
    class Meta:
        verbose_name = 'MCC'
        verbose_name_plural = 'MCC'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title
