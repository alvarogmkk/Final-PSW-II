from django import forms

from .models import Pagamento


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['valor', 'status', 'metodo']
        widgets = {
            'valor': forms.NumberInput(attrs={'step': '0.01'}),
        }
