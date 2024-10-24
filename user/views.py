import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from rest_framework.test import APIRequestFactory
from django.conf import settings

class ProxyUser(APIView):
    def post(self, request, *args, **kwargs):
        try:
            credentials = {
                'email': request.data.get('email'),
                'phone': request.data.get('phone'),
                'password': request.data.get('password')
            }
            response = requests.post(f"{settings.API_SETTINGS.get('CIENTO_URL')}login/",
                                    data = credentials)
            
            if response.status_code == 200:
                return Response(response.json(), status = status.HTTP_200_OK)
            else:
                return Response({'error':'Failed to fetch Ciento API'}, status = response.status_code)
        except requests.exceptions.RequestException as ex:
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            factory = APIRequestFactory()
            proxy_request = factory.post(f"{settings.API_SETTINGS.get('URL')}proxy-login",
                                         data = {
                                             'email': email,
                                             'phone': phone,
                                             'password': password
                                         })
            proxy_user_request = ProxyUser.as_view()
            response = proxy_user_request(proxy_request)
            
            if response.status_code == 200:
                token = response.data['access']

                membership_response = requests.get(
                    f"{settings.API_SETTINGS.get('URL')}membership",
                    headers={'Authorization': f'Bearer {token}'}
                )

                if membership_response.status_code == 200:
                    return HttpResponse(membership_response.json()['results'], status=200)
            else:
                return HttpResponse("Login Failed", status=response.status_code)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
