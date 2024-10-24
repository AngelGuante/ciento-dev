from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label = 'email', max_length = 60)
    phone = forms.CharField(label = 'phone', max_length = 60)
    password = forms.CharField(label = 'password', max_length = 60)