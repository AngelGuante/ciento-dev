import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from .models import Membership
from .serializer import MemberSerializer
from django.conf import settings

class ProxyMembership(APIView):
    def get(self, request, *args, **kwargs):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header:
                return Response({'error': 'Authorization header not provided'}, status=status.HTTP_401_UNAUTHORIZED)

            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            headers = {
                'Authorization': f'Bearer {token}'
            }
            response = requests.get(f"{settings.API_SETTINGS.get('CIENTO_URL')}membership", headers=headers)

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({'error':'Failed to fetch Ciento API'}, status=response.status_code)
        except requests.exceptions.RequestException as ex:
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MembershipListCreateView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MemberSerializer

    def perform_create(self, serializer):
        limit = 5
        membership_count = Membership.objects.count()

        if membership_count >= limit:
            raise({"error": F"Cannot add more memberships, the limit is {limit}."})
        
        serializer.save()

class MembershipDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()
