from django import forms
from django.db.models import Q
from pagamento.models import Pagamento

from .models import Reserva


class ReservaForm(forms.ModelForm):
    metodo_pagamento = forms.ChoiceField(label='Método de pagamento', choices=Pagamento.METODOS, required=False, initial='pix')
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
            'data_entrada': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_saida': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'valor_total': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {'fk_locacao': 'Locação', 'fk_pagamento': 'Pagamento', 'valor_total': 'Valor total (R$)'}

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor_total'].required = False
        self.fields['valor_total'].disabled = True
        self.fields['valor_total'].help_text = 'Calculado automaticamente: diária × quantidade de dias.'
        self.fields['fk_pagamento'].empty_label = 'Gerar pagamento automaticamente'
        permitidos = Q(pk=self.instance.fk_pagamento_id) if self.instance.pk else Q(pk__in=[])
        if usuario and usuario.has_perm('pagamento.change_pagamento'):
            permitidos |= Q(reserva__isnull=True)
        self.fields['fk_pagamento'].queryset = Pagamento.objects.filter(permitidos)
        if self.instance.pk and self.instance.fk_pagamento_id:
            self.fields['metodo_pagamento'].initial = self.instance.fk_pagamento.metodo
        self.diarias = {str(pk): str(valor) for pk, valor in self.fields['fk_locacao'].queryset.values_list('pk', 'preco_diaria')}

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
