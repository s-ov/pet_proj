from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
        Create and return a regular user with an email and password.
    """
    def create_user(self, cell_number, password=None, **extra_fields):
        """
            Create and save a user with the given cell_number and password.
        """
        if not cell_number:
            raise ValueError('The Cell Number field must be set')
        user = self.model(cell_number=cell_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cell_number, password=None, **extra_fields):
        """
            Create and save a superuser with the given cell_number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(cell_number, password, **extra_fields)
        
