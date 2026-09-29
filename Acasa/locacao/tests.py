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


from io import StringIO
from decimal import Decimal
from django.core.management import call_command
from django.contrib.staticfiles import finders
from imagens.models import Imagem
from locacao.models import Locacao
from reserva.models import Reserva


class CatalogoIntegracaoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('popular_demo', stdout=StringIO())

    def test_dez_imoveis_com_campos_e_duas_imagens(self):
        self.assertEqual(Locacao.objects.count(), 10)
        for imovel in Locacao.objects.all():
            self.assertTrue(imovel.disponivel)
            self.assertTrue(imovel.demonstracao)
            self.assertGreater(imovel.preco_mensal, 0)
            self.assertGreater(imovel.area_m2, 0)
            self.assertIsNotNone(imovel.quartos)
            self.assertEqual(imovel.imagens.count(), 2)
            self.assertEqual(imovel.imagens.filter(principal=True).count(), 1)

    def test_carga_repetida_preserva_edicoes_e_nao_duplica(self):
        imovel = Locacao.objects.first()
        imovel.preco_mensal = Decimal('1234.56')
        imovel.save()
        call_command('popular_demo', stdout=StringIO())
        imovel.refresh_from_db()
        self.assertEqual(imovel.preco_mensal, Decimal('1234.56'))
        self.assertEqual(Locacao.objects.count(), 10)
        self.assertEqual(Imagem.objects.count(), 20)

    def test_inicio_e_listagem(self):
        self.assertContains(self.client.get('/'), 'Espaços para viver bem')
        response = self.client.get('/locacoes/')
        self.assertEqual(response.context['page_obj'].paginator.count, 10)
        for imovel in Locacao.objects.all():
            self.assertContains(response, imovel.nome)

    def test_busca_por_nome_cidade_e_endereco(self):
        for query in ['Kitnet', 'Campinas', 'Rua dos Estudantes']:
            response = self.client.get('/locacoes/', {'q': query})
            self.assertEqual(response.context['page_obj'].paginator.count, 1)

    def test_filtros_combinados(self):
        imovel = Locacao.objects.get(nome='Apartamento Parque das Águas')
        response = self.client.get('/locacoes/', {'categoria': imovel.fk_categoria_id,
            'preco_max': '2300', 'quartos': '2', 'status': 'disponivel'})
        self.assertEqual([x.pk for x in response.context['locacoes']], [imovel.pk])

    def test_ordenacao_de_preco(self):
        response = self.client.get('/locacoes/', {'ordenar': 'menor_preco'})
        precos = [x.preco_mensal for x in response.context['locacoes']]
        self.assertEqual(precos, sorted(precos))

    def test_filtro_invalido_exibe_erro_sem_500(self):
        for params in [{'preco_max': 'abc'}, {'categoria': '99999'}, {'quartos': '-1'}, {'ordenar': 'SQL'}]:
            response = self.client.get('/locacoes/', params)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['filtros'].errors)

    def test_resultado_vazio(self):
        response = self.client.get('/locacoes/', {'q': 'inexistente-xyz'})
        self.assertContains(response, 'Nenhum imóvel encontrado')
        self.assertEqual(response.context['page_obj'].paginator.count, 0)

    def test_detalhes_dos_dez_imoveis_e_fotos_locais(self):
        for imovel in Locacao.objects.all():
            response = self.client.get(reverse('detalhar_locacao', args=[imovel.pk]))
            self.assertContains(response, imovel.nome)
            self.assertContains(response, 'Imóvel fictício de demonstração')
            self.assertContains(response, '/ mês')
            self.assertContains(response, '/ diária')
            for foto in imovel.imagens.all():
                self.assertTrue(foto.url_exibicao.startswith('/static/imoveis/'))
                self.assertTrue(finders.find(foto.url_exibicao.removeprefix('/static/')))
                self.assertContains(response, foto.url_exibicao)

    def test_disponibilidade_e_imagem_principal(self):
        imovel = Locacao.objects.first()
        imovel.disponivel = False
        imovel.save()
        principal = imovel.imagens.get(principal=True)
        principal.ordem = 99
        principal.save()
        response = self.client.get(reverse('detalhar_locacao', args=[imovel.pk]))
        self.assertEqual(response.context['imagens'][0].pk, principal.pk)
        self.assertNotContains(response, 'Entrar para reservar')
        response = self.client.get('/locacoes/', {'status': 'indisponivel'})
        self.assertEqual(response.context['page_obj'].paginator.count, 1)

    def test_paginacao_preserva_filtro(self):
        original = Locacao.objects.first()
        for i in range(4):
            Locacao.objects.create(nome=f'Extra {i}', descricao='Campinas', preco_diaria=100,
                capacidade_maxima=2, endereco='Rua teste', local='Campinas', fk_categoria=original.fk_categoria)
        response = self.client.get('/locacoes/', {'status': 'disponivel'})
        self.assertEqual(len(response.context['locacoes']), 12)
        self.assertContains(response, 'status=disponivel&amp;page=2')
        self.assertEqual(len(self.client.get('/locacoes/', {'page': 2}).context['locacoes']), 2)

    def test_reserva_continua_calculada_por_diaria(self):
        usuario = Usuario.objects.create_user(username='reservador', password='segura-123', telefone=11999, CPF=11122233344)
        self.client.force_login(usuario)
        imovel = Locacao.objects.first()
        response = self.client.post('/reservas/criar/', {'fk_locacao': imovel.pk,
            'data_entrada': '2027-02-01', 'data_saida': '2027-02-04', 'status': 'pendente', 'valor_total': ''})
        self.assertEqual(response.status_code, 302)
        reserva = Reserva.objects.get()
        self.assertEqual(reserva.valor_total, 3 * imovel.preco_diaria)
        self.assertEqual(reserva.fk_pagamento.valor, reserva.valor_total)
        self.assertContains(self.client.get(reverse('detalhar_reserva', args=[reserva.pk])), usuario.username)

    def test_crud_admin_com_novos_campos(self):
        admin = Usuario.objects.create_superuser(username='admin-teste', password='segura-123', telefone=123, CPF=55566677788)
        self.client.force_login(admin)
        categoria = Categoria.objects.first()
        dados = {'nome': 'Imóvel teste CRUD', 'descricao': 'Teste', 'preco_diaria': '200',
                 'capacidade_maxima': '4', 'endereco': 'Rua teste', 'local': 'Teste', 'fk_categoria': categoria.pk,
                 'preco_mensal': '2500', 'quartos': '2', 'banheiros': '1', 'vagas_garagem': '0', 'area_m2': '70', 'disponivel': 'on'}
        self.assertEqual(self.client.post(reverse('criar_locacao'), dados).status_code, 302)
        imovel = Locacao.objects.get(nome=dados['nome'])
        self.assertEqual(imovel.preco_mensal, 2500)
        dados['preco_mensal'] = '2600'
        self.assertEqual(self.client.post(reverse('editar_locacao', args=[imovel.pk]), dados).status_code, 302)
        imovel.refresh_from_db()
        self.assertEqual(imovel.preco_mensal, 2600)
        self.assertEqual(self.client.post(reverse('excluir_locacao', args=[imovel.pk])).status_code, 302)
        self.assertFalse(Locacao.objects.filter(pk=imovel.pk).exists())

    def test_imovel_antigo_sem_campos_novos_continua_acessivel(self):
        imovel = Locacao.objects.create(nome='Cadastro antigo', descricao='Preservado',
            preco_diaria=100, capacidade_maxima=2, endereco='Rua teste', local='Teste',
            fk_categoria=Categoria.objects.first())
        response = self.client.get(reverse('detalhar_locacao', args=[imovel.pk]))
        self.assertContains(response, 'Cadastro antigo')
        self.assertNotContains(response, '/ mês')
        self.assertContains(response, '/ diária')

    def test_backend_bloqueia_nova_reserva_de_imovel_indisponivel(self):
        from reserva.forms import ReservaForm
        imovel = Locacao.objects.first()
        imovel.disponivel = False
        imovel.save()
        form = ReservaForm({'fk_locacao': imovel.pk, 'data_entrada': '2027-02-01',
            'data_saida': '2027-02-04', 'status': 'pendente', 'valor_total': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('fk_locacao', form.errors)
