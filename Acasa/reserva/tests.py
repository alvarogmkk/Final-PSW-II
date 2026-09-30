from django.test import TestCase
from django.urls import reverse
from categoria.models import Categoria
from locacao.models import Locacao
from usuario.models import Usuario
from pagamento.models import Pagamento
from pagamento.forms import PagamentoForm
from .models import Reserva
from .forms import ReservaForm


class ReservaCalculoTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(username='cliente-calculo', password='teste-123', CPF=123, telefone=123)
        categoria = Categoria.objects.create(nome='Casa', tipo_locacao='Temporada')
        self.imovel = Locacao.objects.create(nome='Casa teste', descricao='Teste', preco_diaria=199.90,
            capacidade_maxima=4, endereco='Rua teste', local='Teste', fk_categoria=categoria)
        self.client.force_login(self.usuario)
        self.dados = {'data_entrada': '2027-01-01', 'data_saida': '2027-01-04',
            'fk_locacao': self.imovel.pk, 'status': 'pendente', 'valor_total': '0.01', 'metodo_pagamento': 'pix'}

    def test_calcula_total_para_pix_e_cartao_ignorando_valor_enviado(self):
        for metodo in ['pix', 'cartao']:
            response = self.client.post(reverse('criar_reserva'), {**self.dados, 'metodo_pagamento': metodo})
            self.assertEqual(response.status_code, 302)
            reserva = Reserva.objects.latest('pk')
            self.assertEqual(reserva.valor_total, 599.70)
            self.assertEqual(reserva.fk_pagamento.valor, 599.70)
            self.assertEqual(reserva.fk_pagamento.metodo, metodo)

    def test_edicao_recalcula_pagamento_e_preserva_vinculo(self):
        self.client.post(reverse('criar_reserva'), self.dados)
        reserva = Reserva.objects.get()
        pagamento_id = reserva.fk_pagamento_id
        response = self.client.post(reverse('editar_reserva', args=[reserva.pk]), {
            **self.dados, 'data_saida': '2027-01-06', 'fk_pagamento': pagamento_id, 'metodo_pagamento': 'cartao'})
        self.assertEqual(response.status_code, 302)
        reserva.refresh_from_db()
        self.assertEqual(reserva.valor_total, 999.50)
        self.assertEqual(reserva.fk_pagamento.valor, 999.50)
        self.assertEqual(reserva.fk_pagamento_id, pagamento_id)
        self.assertEqual(reserva.fk_pagamento.metodo, 'cartao')
        response = self.client.get(reverse('editar_reserva', args=[reserva.pk]))
        self.assertContains(response, 'value="2027-01-06"')

    def test_datas_invalidas_nao_criam_reserva_nem_pagamento(self):
        for saida in ['2027-01-01', '2026-12-31', 'invalida']:
            response = self.client.post(reverse('criar_reserva'), {**self.dados, 'data_saida': saida})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
        self.assertFalse(Reserva.objects.exists())
        self.assertFalse(Pagamento.objects.exists())

    def test_metodo_invalido_e_pagamento_de_terceiro_sao_recusados(self):
        pagamento = Pagamento.objects.create(valor=1)
        for extra in [{'metodo_pagamento': 'invalido'}, {'fk_pagamento': pagamento.pk}]:
            response = self.client.post(reverse('criar_reserva'), {**self.dados, **extra})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
        self.assertFalse(Reserva.objects.exists())

    def test_rotulos_e_opcoes_de_pagamento(self):
        form = ReservaForm()
        self.assertEqual(form.fields['fk_locacao'].label, 'Locação')
        self.assertEqual(form.fields['fk_pagamento'].label, 'Pagamento')
        self.assertTrue(form.fields['valor_total'].disabled)
        for metodo in ['pix', 'cartao']:
            form = PagamentoForm({'valor': '100', 'status': 'pendente', 'metodo': metodo})
            self.assertTrue(form.is_valid(), form.errors)

    def test_home_simplificada_preserva_filtros_na_listagem(self):
        home = self.client.get(reverse('home'))
        lista = self.client.get(reverse('listar_locacoes'))
        for campo in ['categoria', 'quartos', 'preco_max']:
            self.assertNotIn(campo, home.context['filtros'].fields)
            self.assertIn(campo, lista.context['filtros'].fields)
