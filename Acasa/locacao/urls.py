from django.urls import path

from . import views


urlpatterns = [
    path('', views.listar_locacoes, name='listar_locacoes'),
    path('criar/', views.criar_locacao, name='criar_locacao'),
    path('<int:id>/', views.detalhar_locacao, name='detalhar_locacao'),
    path('<int:id>/editar/', views.editar_locacao, name='editar_locacao'),
    path('<int:id>/excluir/', views.excluir_locacao, name='excluir_locacao'),
]
