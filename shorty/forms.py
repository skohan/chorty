from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Url

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UrlShorteningForm(forms.ModelForm):
    
    class Meta:
        model = Url
        fields = [ 'url', 'slug']
    
    


