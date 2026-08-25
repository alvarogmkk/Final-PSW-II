from django.urls import path

from . import views


urlpatterns = [
    path('', views.listar_reservas, name='listar_reservas'),
    path('criar/', views.criar_reserva, name='criar_reserva'),
    path('<int:id>/', views.detalhar_reserva, name='detalhar_reserva'),
    path('<int:id>/editar/', views.editar_reserva, name='editar_reserva'),
    path('<int:id>/excluir/', views.excluir_reserva, name='excluir_reserva'),
]
