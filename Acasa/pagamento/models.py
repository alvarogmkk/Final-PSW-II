from django.db import models


class Pagamento(models.Model):
    METODOS = [('pix', 'Pix'), ('cartao', 'Cartão')]
    valor = models.FloatField(default=0.0)
    status = models.CharField(max_length=30, default='pendente')
    metodo = models.CharField('método de pagamento', max_length=50, default='pix', choices=METODOS)

    def __str__(self):
        return f"{self.get_metodo_display()} - {self.status}"
