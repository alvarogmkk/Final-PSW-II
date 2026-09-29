from django import forms
from categoria.models import Categoria

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
            'preco_mensal', 'quartos', 'banheiros', 'vagas_garagem', 'area_m2', 'disponivel',
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'preco_diaria': forms.NumberInput(attrs={'step': '0.01'}),
        }


class BuscaLocacaoForm(forms.Form):
    q = forms.CharField(label='Cidade, bairro ou imóvel', required=False, max_length=150,
                        widget=forms.TextInput(attrs={'placeholder': 'Onde você quer morar?'}))
    categoria = forms.ModelChoiceField(label='Tipo de imóvel', queryset=Categoria.objects.order_by('nome'), required=False, empty_label='Todos os tipos')
    preco_max = forms.DecimalField(label='Aluguel mensal até (R$)', required=False, min_value=0, max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'placeholder': 'Sem limite', 'step': '0.01'}))
    quartos = forms.IntegerField(label='Mínimo de quartos', required=False, min_value=0,
                                widget=forms.NumberInput(attrs={'placeholder': 'Qualquer'}))
    status = forms.ChoiceField(label='Disponibilidade', required=False, choices=[('', 'Todos'), ('disponivel', 'Disponível'), ('indisponivel', 'Indisponível')])
    ordenar = forms.ChoiceField(label='Ordenar por', required=False, choices=[('', 'Mais recentes'), ('menor_preco', 'Menor aluguel mensal'), ('maior_preco', 'Maior aluguel mensal'), ('area', 'Maior área')])
