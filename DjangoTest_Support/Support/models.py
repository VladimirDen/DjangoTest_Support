from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


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
    user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=1)
    status = models.ForeignKey(TicketStatus, verbose_name='Статус', on_delete=models.CASCADE, null=False, blank=False)
    type = models.TextField(verbose_name='Тип запроса', max_length=150)
    title = models.CharField(verbose_name='Тема', max_length=250)
    descripion = models.TextField(verbose_name='Описание проблемы', max_length=900)
    created_time = models.DateTimeField(verbose_name='Дата создания', auto_created=True)
    updated_time = models.DateTimeField(verbose_name='Последнее обновление')

    def __str__(self):
        return f'Сообщение для {self.user}| id={self.id}'


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_DEFAULT, default=1)
    message = models.TextField(max_length=150)
