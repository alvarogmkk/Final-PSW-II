from django.db import models

from categoria.models import Categoria


class Locacao(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    preco_diaria = models.FloatField()
    capacidade_maxima = models.IntegerField()
    endereco = models.CharField(max_length=200)
    local = models.CharField(max_length=120)
    fk_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='locacoes')

    def __str__(self):
        return self.nome
