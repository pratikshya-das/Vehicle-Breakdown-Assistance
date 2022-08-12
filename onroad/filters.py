import django_filters
from .models import Business
class RoadFilter(django_filters.FilterSet):
   
    class Meta:
    
        model = Business
        fields = ['city']