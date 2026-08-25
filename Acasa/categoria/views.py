from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm
from .models import Categoria


def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/listar.html', {'categorias': categorias})


def detalhar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categorias/detalhar.html', {'categoria': categoria})


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


def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('detalhar_categoria', id=categoria.id)
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categorias/editar.html', {'form': form, 'categoria': categoria})


def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluida com sucesso!')
        return redirect('listar_categorias')

    return render(request, 'categorias/excluir.html', {'categoria': categoria})
