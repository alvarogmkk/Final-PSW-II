from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    tipo_locacao = models.CharField(max_length=80)

    def __str__(self):
        return self.nome
