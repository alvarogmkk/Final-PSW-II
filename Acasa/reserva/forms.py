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

        locacao = cleaned_data.get('fk_locacao')
        if locacao and not locacao.disponivel and (
            not self.instance.pk or self.instance.fk_locacao_id != locacao.pk
        ):
            self.add_error('fk_locacao', 'Este imóvel não está disponível para novas reservas.')

        return cleaned_data
