from django.contrib import admin

from trucks.models import (Company, Checkin, CompanyLink, Employee, Following,
                           Cuisine)


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