from django.urls import path

from . import views


urlpatterns = [
    path('', views.listar_pagamentos, name='listar_pagamentos'),
    path('criar/', views.criar_pagamento, name='criar_pagamento'),
    path('<int:id>/', views.detalhar_pagamento, name='detalhar_pagamento'),
    path('<int:id>/editar/', views.editar_pagamento, name='editar_pagamento'),
    path('<int:id>/excluir/', views.excluir_pagamento, name='excluir_pagamento'),
]
