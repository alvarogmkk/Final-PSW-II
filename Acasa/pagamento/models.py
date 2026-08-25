from django.db import models


class Pagamento(models.Model):
    valor = models.FloatField(default=0.0)
    status = models.CharField(max_length=30, default='pendente')
    metodo = models.CharField(max_length=50, default='pix')

    def __str__(self):
        return f"{self.metodo} - {self.status}"
