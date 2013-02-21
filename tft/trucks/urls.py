from django.conf.urls import patterns, include, url

from .views import CompanyCuisineList, CompanyDetail, CompanyList

urlpatterns = patterns(
    'trucks.views',
    url(r'^companies/(?P<slug>[-_\w]+)/$', CompanyDetail.as_view(), name='company_detail'),
    url(r'^companies/cuisine/(?P<slug>[-_\w]+)/$', CompanyCuisineList.as_view(), name='company_cuisine_list'),
    url(r'^companies/', CompanyList.as_view(), name='companies'),
)