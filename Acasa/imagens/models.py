from django.db import models
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from urllib.parse import urlsplit

from locacao.models import Locacao


class Imagem(models.Model):
    url = models.URLField(max_length=500)
    descricao = models.CharField(max_length=200, blank=True)
    ordem = models.IntegerField(default=1)
    principal = models.BooleanField(default=False)
    fk_locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE, related_name='imagens')

    def __str__(self):
        return f"Imagem de {self.fk_locacao.nome}"

    @property
    def url_exibicao(self):
        """Use bundled copies of demo photos; keep original URLs editable."""
        origem = urlsplit(self.url)
        if origem.netloc == 'images.unsplash.com':
            nome = origem.path.removeprefix('/')
            if '/' not in nome and nome.startswith('photo-'):
                caminho = f'imoveis/{nome}.jpg'
                if finders.find(caminho):
                    return static(caminho)
        return self.url
