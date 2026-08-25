from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from categoria.models import Categoria

from .forms import LocacaoForm
from .models import Locacao


def home(request):
    locacoes = Locacao.objects.select_related('fk_categoria').all()[:6]
    categorias = Categoria.objects.all()[:6]
    return render(request, 'home/home.html', {'locacoes': locacoes, 'categorias': categorias})


def listar_locacoes(request):
    locacoes = Locacao.objects.select_related('fk_categoria').all()
    return render(request, 'locacoes/listar.html', {'locacoes': locacoes})


def detalhar_locacao(request, id):
    locacao = get_object_or_404(Locacao.objects.select_related('fk_categoria'), pk=id)
    imagens = locacao.imagens.all().order_by('ordem')
    return render(request, 'locacoes/detalhar.html', {'locacao': locacao, 'imagens': imagens})


@login_required
def criar_locacao(request):
    if request.method == 'POST':
        form = LocacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Locacao cadastrada com sucesso!')
            return redirect('listar_locacoes')
    else:
        form = LocacaoForm()

    return render(request, 'locacoes/criar.html', {'form': form})


@login_required
def editar_locacao(request, id):
    locacao = get_object_or_404(Locacao, pk=id)

    if request.method == 'POST':
        form = LocacaoForm(request.POST, instance=locacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Locacao atualizada com sucesso!')
            return redirect('detalhar_locacao', id=locacao.id)
    else:
        form = LocacaoForm(instance=locacao)

    return render(request, 'locacoes/editar.html', {'form': form, 'locacao': locacao})


@login_required
def excluir_locacao(request, id):
    locacao = get_object_or_404(Locacao, pk=id)

    if request.method == 'POST':
        locacao.delete()
        messages.success(request, 'Locacao excluida com sucesso!')
        return redirect('listar_locacoes')

    return render(request, 'locacoes/excluir.html', {'locacao': locacao})
