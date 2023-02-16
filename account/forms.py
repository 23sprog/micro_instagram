from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(min_length=8, max_length=100, widget=forms.PasswordInput(attrs={"class": "form-control"}))


    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("Someone else registered with this email")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("Someone else registered with this username")
        return username

class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(min_length=8, max_length=100, widget=forms.PasswordInput(attrs={"class": "form-control"}))


class ProfileForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ("bio", 'age')