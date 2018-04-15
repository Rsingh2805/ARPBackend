# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class ARPUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Enter username')

        # email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
        return user


class ARPUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('EMP', 'Employee'),
        ('ADM', 'Administrator'),
    )
    MACHINE_STATUS = (
        ('INF', 'Infected'),
        ('SAF', 'Safe'),
    )

    username = models.CharField(max_length=50, unique=True)
    employee_id = models.CharField(max_length=50, unique=True, null=True)
    user_type = models.CharField(
        max_length=3, choices=USER_TYPE, default='EMP', verbose_name='User Type')
    email = models.EmailField(
        verbose_name='Email Address', max_length=255, unique=True, db_index=True)
    phone = models.CharField(max_length=10, verbose_name="Contact Number")
    machine_status = models.CharField(max_length=3, choices=MACHINE_STATUS, default='SAF', verbose_name='PC Status')

    objects = ARPUserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type', 'phone', 'email',
                       'machine_status']
    is_active = models.BooleanField(
        verbose_name='Active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.',
    )
    is_staff = models.BooleanField(
        verbose_name='Staff Status',
        default=False,
        help_text='Check if is staff ',
    )

    def __str__(self):
        return self.email

    def get_name(self):
        return self.username

    class Meta:
        verbose_name_plural = "ARP users"


class Infection(models.Model):
    victim_mac = models.CharField(max_length=100, verbose_name="MAC Address(Victim)")
    victim_ip = models.CharField(max_length=100, verbose_name="IP Address(Victim)")
    pretend_mac = models.CharField(max_length=100, verbose_name="MAC Address(Pretend)")
    pretend_ip = models.CharField(max_length=100, verbose_name="IP Address(Pretend)")
    victim_employee = models.ForeignKey(ARPUser, on_delete=models.SET_NULL, null=True, verbose_name="Victim", related_name="infections")
    timestamp = models.DateTimeField(verbose_name="Date/Time of Infection")

    def __str__(self):
        return self.victim_employee.username + ' Infection'


class Message(models.Model):
    MESSAGE_TYPE = (
        ('INF', 'Infection'),
        ('FIX', 'Fixed')
    )
    message_type = models.CharField(choices=MESSAGE_TYPE, max_length=3)
    victim_id = models.ForeignKey(ARPUser, on_delete=models.SET_NULL, null=True, related_name="messages")
    timestamp = models.DateTimeField(verbose_name="Date/Time")


