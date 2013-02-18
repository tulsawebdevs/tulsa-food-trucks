from django.conf.urls import patterns, include, url

from .views import TruckList, TruckDetail

urlpatterns = patterns(
    'trucks.views',
    url(r'^companies/(?P<slug>[-_\w]+)/$', TruckDetail.as_view(), name='company_detail'),
    url(r'^companies/', TruckList.as_view(), name='companies'),
)