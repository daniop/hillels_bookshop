from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Client, Review


class SearchForm(forms.Form):
    query = forms.CharField(label='')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=30)
    email = forms.EmailField(label='Email', max_length=30)
    message = forms.CharField(label='Сообщение', max_length=300)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'body']


class ClientCreationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ("username", "email", "password1", "password2")


class ClientChangeForm(UserChangeForm):
    class Meta:
        model = Client
        fields = ("username", "email", 'first_name', 'address', 'city', 'postal_code')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Логин')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Пароль')
