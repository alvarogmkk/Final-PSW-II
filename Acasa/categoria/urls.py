from django.urls import path

from . import views


urlpatterns = [
    path('', views.listar_categorias, name='listar_categorias'),
    path('criar/', views.criar_categoria, name='criar_categoria'),
    path('<int:id>/', views.detalhar_categoria, name='detalhar_categoria'),
    path('<int:id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('<int:id>/excluir/', views.excluir_categoria, name='excluir_categoria'),
]
