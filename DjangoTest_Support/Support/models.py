from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    users = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return f'{self.users}'


class TicketStatus(models.Model):
    STATUSES = [
        ('Activ', 'Activ'),
        ('In_work', 'In_work'),
        ('Сompleted', 'Сompleted')
        ]

    status = models.CharField(max_length=15, choices=STATUSES, unique=True)

    @property
    def in_loft(self):
        return self.status == 'Activ' or self.status == 'Сompleted'


class Ticket(models.Model):
    utilizer = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    status = models.ForeignKey(TicketStatus, verbose_name='Статус', on_delete=models.CASCADE, null=False, blank=False)
    type = models.TextField(verbose_name='Тип запроса', max_length=150)
    title = models.CharField(verbose_name='Тема', max_length=250)
    descripion = models.TextField(verbose_name='Описание проблемы', max_length=900)
    created_time = models.DateTimeField(verbose_name='Дата создания', auto_created=True)
    updated_time = models.DateTimeField(verbose_name='Последнее обновление')

    def __str__(self):
        return f'Сообщение для {self.utilizer.users}| id={self.id}'


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_DEFAULT, default=1)
    message = models.TextField(max_length=150)
