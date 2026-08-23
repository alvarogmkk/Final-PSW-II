from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    path('locacoes/', views.listar_locacoes, name='listar_locacoes'),
    path('locacoes/criar/', views.criar_locacao, name='criar_locacao'),
    path('locacoes/<int:id>/', views.detalhar_locacao, name='detalhar_locacao'),
    path('locacoes/<int:id>/editar/', views.editar_locacao, name='editar_locacao'),
    path('locacoes/<int:id>/excluir/', views.excluir_locacao, name='excluir_locacao'),
    path('reservas/', views.listar_reservas, name='listar_reservas'),
    path('reservas/criar/', views.criar_reserva, name='criar_reserva'),
    path('reservas/<int:id>/', views.detalhar_reserva, name='detalhar_reserva'),
    path('usuarios/cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('usuarios/login/', views.login_usuario, name='login_usuario'),
    path('usuarios/logout/', views.logout_usuario, name='logout_usuario'),
]
