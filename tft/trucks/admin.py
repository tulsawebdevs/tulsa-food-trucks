from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from trucks.models import (Company, Checkin, CompanyLink, Employee, Following,
                           Cuisine, Profile)

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = "Profiles"
    verbose_name = "Profile"
    can_delete = False


class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email',
                    'is_active', 'is_staff', 'profile_phone_confirmed',
                    'profile_email_confirmed',)
    inlines = (ProfileInline,)

    def profile_phone_confirmed(self, obj):
        return obj.profile.phone_confirmed or False
    profile_phone_confirmed.boolean = True
    profile_phone_confirmed.short_description = 'Phone Conf?'

    def profile_email_confirmed(self, obj):
        return obj.profile.email_confirmed
    profile_email_confirmed.boolean = True or False
    profile_email_confirmed.short_description = 'Email Conf?'


admin.site.register(User, UserProfileAdmin)


class EmployeeInline(admin.StackedInline):
    model = Employee


class LinkInline(admin.StackedInline):
    model = CompanyLink


class CompanyAdmin(admin.ModelAdmin):
    inlines = (EmployeeInline, LinkInline)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Checkin)
admin.site.register(Following)
admin.site.register(Cuisine)