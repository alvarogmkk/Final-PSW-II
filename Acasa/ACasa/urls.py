from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('locacao.urls')),
    path('categorias/', include('categoria.urls')),
    path('imagens/', include('imagens.urls')),
    path('pagamentos/', include('pagamento.urls')),
    path('usuarios/', include('usuario.urls')),
    path('reservas/', include('reserva.urls')),
    path('admin/', admin.site.urls),
]
