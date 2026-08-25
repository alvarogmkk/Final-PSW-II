from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CategoriaForm
from .models import Categoria


def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/listar.html', {'categorias': categorias})


@login_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'categorias/criar.html', {'form': form})
