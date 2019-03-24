import django_filters
from .models import Cursos


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Cursos
        fields = ['uf', 'curso' ]
