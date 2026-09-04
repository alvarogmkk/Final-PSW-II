from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from categoria.models import Categoria
from usuario.models import Usuario


class LocacaoPermissionTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='sem-permissao',
            password='senha-segura-123',
            telefone=11988888888,
            CPF=98765432100,
        )

    def test_criacao_de_locacao_exige_permissao_do_modelo(self):
        self.client.force_login(self.usuario)
        url = reverse('criar_locacao')

        self.assertEqual(self.client.get(url).status_code, 403)

        permissao = Permission.objects.get(codename='add_locacao')
        self.usuario.user_permissions.add(permissao)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_locacoes_sao_publicas_para_consulta(self):
        Categoria.objects.create(nome='Casa', tipo_locacao='Temporada')

        self.assertEqual(self.client.get(reverse('listar_locacoes')).status_code, 200)
