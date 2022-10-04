from django import forms

from .models import Review


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
