from django.contrib.auth.models import User
from django.db import models


class Usuario(User):
    telefone = models.BigIntegerField()
    CPF = models.BigIntegerField(unique=True)
    criado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name() or self.username
