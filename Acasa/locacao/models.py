from django.db import models
from django.core.validators import MinValueValidator

from categoria.models import Categoria


class Locacao(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    preco_diaria = models.FloatField()
    capacidade_maxima = models.IntegerField()
    endereco = models.CharField(max_length=200)
    local = models.CharField(max_length=120)
    fk_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='locacoes')
    preco_mensal = models.DecimalField('aluguel mensal', max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.01)])
    quartos = models.PositiveSmallIntegerField(null=True, blank=True)
    banheiros = models.PositiveSmallIntegerField(null=True, blank=True)
    vagas_garagem = models.PositiveSmallIntegerField('vagas de garagem', null=True, blank=True)
    area_m2 = models.DecimalField('área em m²', max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.01)])
    disponivel = models.BooleanField('disponível para locação', default=True)
    demonstracao = models.BooleanField('imóvel de demonstração', default=False, editable=False)

    def __str__(self):
        return self.nome
