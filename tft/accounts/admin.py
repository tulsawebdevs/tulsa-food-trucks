from django.contrib import admin
# from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import  PhoneVerification, EmailVerification, User

# admin.site.unregister(User)

# class ProfileInline(admin.StackedInline):
#     model = Profile
#     verbose_name_plural = "Profiles"
#     verbose_name = "Profile"
#     can_delete = False
# 
# 
class AccountUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'email')
    ordering = ('email',)
#     list_display = ('username', 'first_name', 'last_name', 'email',
#                     'is_active', 'is_staff', 'profile_phone_confirmed',
#                     'profile_email_confirmed',)
#     inlines = (ProfileInline,)
# 
#     def profile_phone_confirmed(self, obj):
#         return obj.profile.phone_confirmed or False
#     profile_phone_confirmed.boolean = True
#     profile_phone_confirmed.short_description = 'Phone Conf?'
# 
#     def profile_email_confirmed(self, obj):
#         return obj.profile.email_confirmed
#     profile_email_confirmed.boolean = True or False
#     profile_email_confirmed.short_description = 'Email Conf?'


admin.site.register(User, AccountUserAdmin)
# admin.site.register(User)

admin.site.register(PhoneVerification)
admin.site.register(EmailVerification)