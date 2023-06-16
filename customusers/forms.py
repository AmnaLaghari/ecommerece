# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import CustomUser

class SignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "profile")