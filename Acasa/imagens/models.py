from django.db import models

from locacao.models import Locacao


class Imagem(models.Model):
    url = models.URLField(max_length=500)
    descricao = models.CharField(max_length=200, blank=True)
    ordem = models.IntegerField(default=1)
    principal = models.BooleanField(default=False)
    fk_locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE, related_name='imagens')

    def __str__(self):
        return f"Imagem de {self.fk_locacao.nome}"
