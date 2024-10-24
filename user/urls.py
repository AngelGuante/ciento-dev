from django.urls import path
from .views import ProxyUser, login_view

urlpatterns = [
    path('proxy-login/', ProxyUser.as_view(), name = 'proxy-login'),
    path('', login_view, name = 'login'),
]