from django.contrib.auth.models import User
from django.db import models


class Usuario(models.Model):
    telefone = models.CharField(max_length=20)
    CPF = models.CharField(max_length=11, unique=True)
    criado_em = models.DateField(auto_now_add=True)
    fk_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    def __str__(self):
        return self.fk_user.get_full_name() or self.fk_user.username


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    tipo_locacao = models.CharField(max_length=80)

    def __str__(self):
        return self.nome


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


class Pagamento(models.Model):
    valor = models.FloatField(default=0.0)
    status = models.CharField(max_length=30, default='pendente')
    metodo = models.CharField(max_length=50, default='pix')

    def __str__(self):
        return f"{self.metodo} - {self.status}"


class Reserva(models.Model):
    data_entrada = models.DateField()
    data_saida = models.DateField()
    valor_total = models.FloatField(default=0.0)
    status = models.CharField(max_length=30, default='pendente')
    fk_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='reservas')
    fk_locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE, related_name='reservas')
    fk_pagamento = models.OneToOneField(Pagamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='reserva')

    def __str__(self):
        return f"Reserva {self.id} - {self.fk_locacao.nome}"
