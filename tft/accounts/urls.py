from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'accounts.views',
    url(r'^register/$', 'register', name='register'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    
    url(r'^register/phone/$', 'register_phone', name='register_phone'),
    url(r'^register/email/$', 'register_email', name='register_email'),
)