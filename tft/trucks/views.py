from django.views.generic import ListView, DetailView
from .models import Company


class TruckList(ListView):
 
    template_name = 'trucks/company_list.html'

    model = Company

    context_object_name = 'companies'


class TruckDetail(DetailView):

    template_name = 'trucks/company_detail.html'

    slug_field = 'slug'

    model = Company

    context_object_name = 'company'
    