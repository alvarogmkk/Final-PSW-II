from django import forms

from .models import Imagem


class ImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        fields = ['url', 'descricao', 'ordem', 'principal', 'fk_locacao']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descricao da imagem'}),
        }
