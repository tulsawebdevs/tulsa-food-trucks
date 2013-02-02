from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField

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
        return "%s's profile" % self.user

    @staticmethod
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(Profile.create_user_profile, sender=User)


class Cuisine(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name', overwrite=True)


class Company(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField()
    cuisine = models.ManyToManyField(Cuisine)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Companies'

class CompanyLink(models.Model):
    company = models.ForeignKey(Company)
    url = models.URLField()
    TYPE_CHOICES = (('fb', 'facebook'), ('tw', 'twitter'),
                    ('us', 'urban spoon'), ('y', 'yelp'), ('web', 'website'))
    link_type = models.CharField(max_length=5, choices=TYPE_CHOICES)


class Following(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    notify = models.BooleanField(default=True)


class Employee(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(User)
    OWNER = 0
    EMPLOYEE = 1
    TITLE_CHOICES = ((OWNER, 'owner'), (EMPLOYEE, 'employee'),)
    title = models.IntegerField(choices=TITLE_CHOICES, default=EMPLOYEE)

class Checkin(TimeStampedModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    company = models.ForeignKey(Company)
    created_by = models.ForeignKey(User)
    