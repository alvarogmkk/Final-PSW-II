import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from categoria.models import Categoria
from imagens.models import Imagem
from locacao.models import Locacao


class Command(BaseCommand):
    help = 'Adiciona dez imóveis fictícios sem sobrescrever cadastros existentes.'

    @transaction.atomic
    def handle(self, *args, **options):
        arquivo = Path(__file__).resolve().parents[2] / 'fixtures' / 'demo_locacoes.json'
        registros = json.loads(arquivo.read_text(encoding='utf-8'))
        categorias, locacoes = {}, {}
        criados = 0
        for registro in registros:
            campos = registro['fields'].copy()
            if registro['model'] == 'categoria.categoria':
                categoria = Categoria.objects.filter(nome=campos['nome']).order_by('pk').first()
                if categoria is None:
                    categoria = Categoria.objects.create(**campos)
                categorias[registro['pk']] = categoria
            elif registro['model'] == 'locacao.locacao':
                campos['fk_categoria'] = categorias[campos['fk_categoria']]
                existente = Locacao.objects.filter(nome=campos['nome'], demonstracao=True).order_by('pk').first()
                if existente is None:
                    existente = Locacao.objects.create(**campos)
                    criados += 1
                    locacoes[registro['pk']] = existente
            elif registro['model'] == 'imagens.imagem':
                locacao = locacoes.get(campos.pop('fk_locacao'))
                if locacao is not None:
                    Imagem.objects.create(fk_locacao=locacao, **campos)
        self.stdout.write(self.style.SUCCESS(f'{criados} imóveis de demonstração adicionados. Cadastros existentes preservados.'))
