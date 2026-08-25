from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['telefone', 'CPF']


class CadastroForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=20)
    CPF = forms.CharField(max_length=11)

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'telefone',
            'CPF',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.telefone = self.cleaned_data['telefone']
        user.CPF = self.cleaned_data['CPF']

        if commit:
            user.save()

        return user
