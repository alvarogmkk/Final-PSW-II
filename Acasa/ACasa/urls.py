from django.contrib import admin
from django.urls import include, path

from locacao import views as locacao_views

urlpatterns = [
    path('', locacao_views.home, name='home'),
    path('categorias/', include('categoria.urls')),
    path('locacoes/', include('locacao.urls')),
    path('reservas/', include('reserva.urls')),
    path('usuarios/', include('usuario.urls')),
    path('admin/', admin.site.urls),
]
