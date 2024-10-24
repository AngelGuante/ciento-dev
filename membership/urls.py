from django.urls import path
from .views import ProxyMembership, MembershipListCreateView, MembershipDetailView

urlpatterns = [
    path('', ProxyMembership.as_view(), name='membership'),
    path('list/', MembershipListCreateView.as_view(), name = 'membership_list_create'),
    path('<int:id>/', MembershipDetailView.as_view(), name = 'membership_detail')
]