# accounts/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    profile = forms.FileField(label=_('Profile'), widget=forms.FileInput)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "profile")