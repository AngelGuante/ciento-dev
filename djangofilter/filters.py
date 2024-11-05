import django_filters
from .models import Test

class TestFilter(django_filters.rest_framework.FilterSet):
    field1 = django_filters.CharFilter(field_name = 'field1', lookup_expr = 'icontains')

    class Meta:
        model = Test
        fields = ['field1']