from .models import Cuisine

def categoryContext(request=None):
    """add the category to the request context"""
    return {
        'cuisines': Cuisine.objects.all()
    }