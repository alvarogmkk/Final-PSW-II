from django.test import TestCase
from django.urls import reverse

from .models import Usuario


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='cliente',
            password='senha-segura-123',
            telefone=11999999999,
            CPF=12345678901,
        )

    def test_login_cria_sessao_autenticada(self):
        response = self.client.post(
            reverse('login_usuario'),
            {'username': 'cliente', 'password': 'senha-segura-123'},
        )

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.client.session['_auth_user_id'], str(self.usuario.pk))

    def test_reservas_exigem_login(self):
        response = self.client.get(reverse('listar_reservas'))

        self.assertRedirects(
            response,
            f"{reverse('login_usuario')}?next={reverse('listar_reservas')}",
        )

    def test_login_retorna_para_rota_original(self):
        destino = reverse('listar_reservas')
        response = self.client.post(
            reverse('login_usuario'),
            {'username': 'cliente', 'password': 'senha-segura-123', 'next': destino},
        )

        self.assertRedirects(response, destino)

    def test_logout_exige_post_e_encerra_sessao(self):
        self.client.force_login(self.usuario)

        self.assertEqual(self.client.get(reverse('logout_usuario')).status_code, 405)
        response = self.client.post(reverse('logout_usuario'))

        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)


    def test_edicao_preserva_senha_e_nao_permite_auto_conceder_permissoes(self):
        from django.contrib.auth.models import Permission
        permissao = Permission.objects.get(codename='add_locacao')
        self.client.force_login(self.usuario)
        response = self.client.post(reverse('editar_usuario', args=[self.usuario.pk]), {
            'username': self.usuario.username, 'telefone': self.usuario.telefone,
            'CPF': self.usuario.CPF, 'password': '', 'user_permissions': [permissao.pk]})
        self.assertEqual(response.status_code, 302)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password('senha-segura-123'))
        self.assertFalse(self.usuario.has_perm('locacao.add_locacao'))
