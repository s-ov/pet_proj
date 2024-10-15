from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """The base class for custom user creation, handling authentication and authorization."""

    cell_number_validator = RegexValidator(
        regex=r'^\+38(050|066|095|099|067|068|096|097|098|063|073|093|091)\d{7}$',
        message="Номер має бути '+38', потім код оператора, а потім ще 7 цифр номеру. Наприклад: +380501234567"
    )

    username = None
    cell_number = models.CharField(
        unique=True, 
        validators=[cell_number_validator],
        max_length=15, 
        verbose_name='Мобільний',
        )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )

    USERNAME_FIELD = "cell_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """Return string representation for user."""
        return f"{self.first_name} {self.last_name}"


class Employee(CustomUser):
    """The class for employees, handling specific employee roles."""

    class Role(models.TextChoices):
        ENGINEER = 'Engineer', 'Інженер'
        ELECTRICIAN = 'Electrician', 'Електрик'

    class AdmissionGroup(models.TextChoices):
        GROUP_I = 'І-ша група з електробезпеки', 'I'
        GROUP_II = 'ІI-а група з електробезпеки', 'II'
        GROUP_III = 'ІII-тя група з електробезпеки', 'III'
        GROUP_IV_BELOW_1KV = 'ІV-а до 1000V група з електробезпеки', 'IV до 1kV'
        GROUP_IV_ABOVE_1KV = 'ІV-а вище 1000V група з електробезпеки', 'IV вище 1kV'
        GROUP_V = 'V-а група з електробезпеки', 'V'
        NONE = 'Не вибрано', 'Не вибрано'

    role = models.CharField(max_length=15, choices=Role.choices, default=Role.ELECTRICIAN)
    admission_group = models.CharField(
        max_length=130, 
        choices=AdmissionGroup.choices, 
        default=AdmissionGroup.NONE, 
        blank=True, null=True,
        )

    def __str__(self):
        """Return string representation for employee."""
        return f"{self.get_role_display()} - {self.first_name} {self.last_name}"
