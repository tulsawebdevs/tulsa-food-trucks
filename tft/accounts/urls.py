from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from .views import RegistrationView

urlpatterns = patterns(
    'accounts.views',
    url(r'^register/$', RegistrationView.as_view(), name='accounts_register'),
    url(r'^login/$', 'login', name='accounts_login'),
    url(r'^logout/$', 'logout', name='accounts_logout'),
    url(r'^activate/$', TemplateView.as_view(template_name='accounts/activate.jinja'), name='accounts_activate'),
    url(r'^register/phone/$', 'register_phone', name='accounts_register_phone'),
    url(r'^register/email/$', 'register_email', name='accounts_register_email'),
)