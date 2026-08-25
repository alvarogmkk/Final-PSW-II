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


class Imagem(models.Model):
    url = models.URLField(max_length=500)
    descricao = models.CharField(max_length=200, blank=True)
    ordem = models.IntegerField(default=1)
    principal = models.BooleanField(default=False)
    fk_locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE, related_name='imagens')

    def __str__(self):
        return f"Imagem de {self.fk_locacao.nome}"
