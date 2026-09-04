from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('locacoes/', views.listar_locacoes, name='listar_locacoes'),
    path('locacoes/criar/', views.criar_locacao, name='criar_locacao'),
    path('locacoes/<int:id>/', views.detalhar_locacao, name='detalhar_locacao'),
    path('locacoes/<int:id>/editar/', views.editar_locacao, name='editar_locacao'),
    path('locacoes/<int:id>/excluir/', views.excluir_locacao, name='excluir_locacao'),
]
