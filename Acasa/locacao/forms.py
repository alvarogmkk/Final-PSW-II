from django import forms

from .models import Imagem, Locacao


class ImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        fields = ['url', 'descricao', 'ordem', 'principal']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descricao da imagem'}),
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
