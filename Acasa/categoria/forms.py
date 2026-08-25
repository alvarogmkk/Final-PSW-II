from django import forms

from .models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'tipo_locacao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
