from django.urls import path

from . import views


urlpatterns = [
    path('', views.listar_categorias, name='listar_categorias'),
    path('criar/', views.criar_categoria, name='criar_categoria'),
]
