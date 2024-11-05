from rest_framework import generics
from .models import Test
from .serializers import TestSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TestFilter

class TestListCreateAPIView(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TestFilter
