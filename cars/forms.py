from django import forms
from .models import Car, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'description']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Только поле содержимого комментария

    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ваш комментарий...'}), label="Комментарий")