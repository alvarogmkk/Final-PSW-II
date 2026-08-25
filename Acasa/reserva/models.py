from django.db import models

from locacao.models import Locacao
from pagamento.models import Pagamento
from usuario.models import Usuario


class Reserva(models.Model):
    data_entrada = models.DateField()
    data_saida = models.DateField()
    valor_total = models.FloatField(default=0.0)
    status = models.CharField(max_length=30, default='pendente')
    fk_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    fk_locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE, related_name='reservas')
    fk_pagamento = models.OneToOneField(Pagamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='reserva')

    def __str__(self):
        return f"Reserva {self.id} - {self.fk_locacao.nome}"
