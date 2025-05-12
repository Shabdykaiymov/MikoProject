# users/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']

        class ProfileUpdateForm(forms.ModelForm):
            class Meta:
                model = Profile
                fields = ['phone', 'address']
                widgets = {
                    'phone': forms.TextInput(attrs={'class': 'form-control'}),
                    'address': forms.TextInput(attrs={'class': 'form-control'}),
                }