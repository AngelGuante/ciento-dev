from django.urls import path
from .views import TestListCreateAPIView

urlpatterns = [
    path('', TestListCreateAPIView.as_view(), name = 'list_test')
]