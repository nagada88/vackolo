import django_filters
from .models import Allat

class AllatFilter(django_filters.FilterSet):
    
    class Meta:
        model = Allat     
        fields = {'faj': ['exact'], 'meret': ['exact'], 'ivar': ['exact']}
        
    