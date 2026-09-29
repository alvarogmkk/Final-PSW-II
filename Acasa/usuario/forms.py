from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha',
        required=False,
        widget=forms.PasswordInput(),
        help_text='Obrigatoria para criar usuario. Deixe em branco para manter a senha atual.',
    )

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'telefone',
            'CPF',
            'groups',
            'user_permissions',
        ]
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
            'user_permissions': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, permitir_permissoes=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._senha_original = self.instance.password
        self.fields['password'].required = self.instance.pk is None
        if not permitir_permissoes:
            self.fields.pop('groups')
            self.fields.pop('user_permissions')

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            usuario.set_password(password)
        else:
            usuario.password = self._senha_original

        if commit:
            usuario.save()
            self.save_m2m()

        return usuario


class CadastroForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    telefone = forms.IntegerField()
    CPF = forms.IntegerField()

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
        user.first_name = self.cleaned_data.get('Primeiro Nome', '')
        user.last_name = self.cleaned_data.get('Segundo Nome', '')
        user.telefone = self.cleaned_data['telefone']
        user.CPF = self.cleaned_data['CPF']

        if commit:
            user.save()

        return user
