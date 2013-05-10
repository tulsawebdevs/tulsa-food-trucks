from django.conf.urls import patterns, include, url
from django.contrib import admin

from trucks.views import HomeCompanyList

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    
	url(r'^$', HomeCompanyList.as_view(), name="home"),
    url(r'^', include('accounts.urls')),
    url(r'^', include('trucks.urls')),
    url(r'^', include('waffle.urls')),
)
