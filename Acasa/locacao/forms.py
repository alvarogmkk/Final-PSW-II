from django import forms

from .models import Locacao


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
