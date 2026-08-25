from django import forms

from .models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'data_entrada',
            'data_saida',
            'valor_total',
            'status',
            'fk_usuario',
            'fk_locacao',
            'fk_pagamento',
        ]
        widgets = {
            'data_entrada': forms.DateInput(attrs={'type': 'date'}),
            'data_saida': forms.DateInput(attrs={'type': 'date'}),
            'valor_total': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor_total'].required = False

    def clean(self):
        cleaned_data = super().clean()
        data_entrada = cleaned_data.get('data_entrada')
        data_saida = cleaned_data.get('data_saida')

        if data_entrada and data_saida and data_saida <= data_entrada:
            raise forms.ValidationError('A data de saida deve ser maior que a data de entrada.')

        return cleaned_data
