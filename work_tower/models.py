from django.db import models
from django.core.exceptions import ValidationError


class WorkTowerLevel(models.Model):
    """
        The model represents levels on the work tower
    """
    LEVELS = [
        (4.8, '4.8m'),
        (8.0, '8.0m'),
        (11.2, '11.2m'),
        (15.4, '15.4m'),
        (21.0, '21.0m'),
        (25.5, '25.5m'),
        (28.0, '28.0m'),
        (32.1, '32.1m'),
        (36.6, '36.6m'),
        (41.0, '41.0m'),
        (41.01, '41.0.m: над силосами 6.1-6.6'),
        (41.02, '41.0.m: над силосами 6.7-6.12'),
    ]
    level = models.FloatField(max_length=100, choices=[(x[0], x[1]) for x in LEVELS], default=0.0)

    class Meta:
        verbose_name = 'Рівень'
        verbose_name_plural = 'Рівні робочої вежі'

    def clean(self):
        """Custom validation: check that the level is valid"""
        super().clean()
        if self.level not in dict(self.LEVELS):
            raise ValidationError(f'Invalid level: {self.level}. Must be one of {dict(self.LEVELS)}.')

    def __str__(self):
        return str(self.level)
