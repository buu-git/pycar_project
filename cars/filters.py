import django_filters
from cars.models import Car

class CarsFilter(django_filters.FilterSet):
    class Meta:
        model = Car
        fields = {'car_type': ['exact']
        }