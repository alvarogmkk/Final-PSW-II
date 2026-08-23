from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Categoria, Imagem, Locacao, Reserva, Usuario


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'tipo_locacao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }


class ImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        fields = ['url', 'descricao', 'ordem', 'principal']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da imagem'}),
        }


class LocacaoForm(forms.ModelForm):
    class Meta:
        model = Locacao
        fields = [
            'nome',
            'descricao',
            'preco_diaria',
            'capacidade_maxima',
            'endereco',
            'local',
            'fk_categoria',
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'preco_diaria': forms.NumberInput(attrs={'step': '0.01'}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data_entrada', 'data_saida', 'fk_locacao']
        widgets = {
            'data_entrada': forms.DateInput(attrs={'type': 'date'}),
            'data_saida': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_entrada = cleaned_data.get('data_entrada')
        data_saida = cleaned_data.get('data_saida')

        if data_entrada and data_saida and data_saida <= data_entrada:
            raise forms.ValidationError('A data de saída deve ser maior que a data de entrada.')

        return cleaned_data


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
        model = get_user_model()
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

        if commit:
            user.save()
            Usuario.objects.create(
                fk_user=user,
                telefone=self.cleaned_data['telefone'],
                CPF=self.cleaned_data['CPF'],
            )

        return user
