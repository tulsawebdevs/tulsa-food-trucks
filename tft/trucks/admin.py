from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from trucks.models import (Company, Checkin, CompanyLink, Employee, Following,
                           Cuisine, Profile)


admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserProfileAdmin(UserAdmin):
    inlines = (ProfileInline,)


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