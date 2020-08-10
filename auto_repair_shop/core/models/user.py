
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.managers import IsDeletedModel

__all__ = (
    'User',
    'UserCar',
)


class UserManager(BaseUserManager):
    def create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(password, **extra_fields)


class User(AbstractUser):
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserCar(IsDeletedModel):
    owner = models.ForeignKey("User", verbose_name=_("Car owner"), on_delete=models.CASCADE)
    model = models.CharField(max_length=64, verbose_name=_('Car model'), null=True, blank=True)
    plate_num = models.CharField(max_length=16, verbose_name=_('Plate number'), null=True, blank=True)

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    def __str__(self):
        model = "{} ".format(self.model) if self.model else ""
        plate_num = "{} ".format(self.plate_num) if self.plate_num else ""
        return f"{model}{plate_num}({self.owner.get_full_name()})"
