import random
import string

from django.conf import settings
# from django.contrib.auth.models import User
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
    BaseUserManager)

from django.core.mail import send_mail

from django.db import models
from django.db.models import EmailField
from django.db.models.signals import post_save
from django.utils import timezone

from django_localflavor_us.models import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_staff=False, is_active=True,
                          is_superuser=False, last_login=now, **extra_fields)
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailField('email address', max_length=254, unique=True,
        help_text='Emails are used to log in to the app')
    phone = PhoneNumberField('phone number', unique=True,
        help_text='Phone numbers are used to send a text message to a user'
                  'if they choose to be notified that way.')
    date_of_birth = models.DateField('date of birth', blank=True, null=True,
        help_text='Birthday can eventually be used by food trucks for'
                  'promotions.')
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                  'site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as '
                  'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    phone_confirmed = models.BooleanField(default=False,
        help_text='User has confirmed their phone number.')
    email_confirmed = models.BooleanField(default=False,
        help_text='User has confirmed their email address.')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class VerificationBase(models.Model):
    code = models.CharField(max_length=6)
    sent_at = models.DateTimeField()

    class Meta:
        abstract = True

    def send(self):
        raise NotImplemented()

    @staticmethod
    def random_code():
        return ''.join(random.sample(string.digits, 6))

    @classmethod
    def create_with_unique_code(cls, value):
        code = cls.random_code()
        while cls.objects.filter(code=code).exists():
            code = cls.random_code()
        obj = cls.objects.create(
            value=value, code=code, sent_at=datetime.now())
        obj.send()
        return obj


class PhoneVerification(VerificationBase):
    value = PhoneNumberField()

    def send(self):
        send_msg(
            self.value,
            'To verify your phone w/ tfdd.co, please visit %s%s?code=%s .' % (
                settings.BASE_URL, reverse('register_phone'), self.code))


class EmailVerification(VerificationBase):
    value = models.EmailField()

    def send(self):
        send_mail(
            'Registration',
            'To verify your email, please visit %s%s?code=%s .' % (
                settings.BASE_URL, reverse('register_email'), self.code),
            'no-reply@tulsafoodtrucks.com', [self.value], fail_silently=True)