from django.urls import path

from imagens import views


urlpatterns = [
    path('', views.listar_imagens, name='listar_imagens'),
    path('criar/', views.criar_imagem, name='criar_imagem'),
    path('<int:id>/', views.detalhar_imagem, name='detalhar_imagem'),
    path('<int:id>/editar/', views.editar_imagem, name='editar_imagem'),
    path('<int:id>/excluir/', views.excluir_imagem, name='excluir_imagem'),
]

