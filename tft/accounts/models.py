import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField

from django.core.mail import send_mail

from django.db import models
from django.db.models.signals import post_save


# from tfdd
class Profile(models.Model):
    """Additional User data"""
    user = models.OneToOneField(User)
    phone = PhoneNumberField()
    phone_confirmed = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return "%s %s's profile" % (self.user.first_name,
                                        self.user.last_name,)
        else:
            return "%s's profile" % self.user

    def save(self, *args, **kwargs):
        try:
            existing = Profile.objects.get(user=self.user)
            self.id = existing.id #force update instead of insert
        except Profile.DoesNotExist:
            pass 
        models.Model.save(self, *args, **kwargs)

    @staticmethod
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(Profile.create_user_profile, sender=User)


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