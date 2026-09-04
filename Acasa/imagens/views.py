from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ImagemForm
from .models import Imagem


def listar_imagens(request):
    imagens = Imagem.objects.select_related('fk_locacao').all()
    return render(request, 'imagens/listar.html', {'imagens': imagens})


def detalhar_imagem(request, id):
    imagem = get_object_or_404(Imagem.objects.select_related('fk_locacao'), pk=id)
    return render(request, 'imagens/detalhar.html', {'imagem': imagem})


@permission_required('imagens.add_imagem', raise_exception=True)
def criar_imagem(request):
    if request.method == 'POST':
        form = ImagemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Imagem cadastrada com sucesso!')
            return redirect('listar_imagens')
    else:
        initial = {}
        locacao_id = request.GET.get('locacao')
        if locacao_id:
            initial['fk_locacao'] = locacao_id

        form = ImagemForm(initial=initial)

    return render(request, 'imagens/criar.html', {'form': form})


@permission_required('imagens.change_imagem', raise_exception=True)
def editar_imagem(request, id):
    imagem = get_object_or_404(Imagem, pk=id)

    if request.method == 'POST':
        form = ImagemForm(request.POST, instance=imagem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Imagem atualizada com sucesso!')
            return redirect('detalhar_imagem', id=imagem.id)
    else:
        form = ImagemForm(instance=imagem)

    return render(request, 'imagens/editar.html', {'form': form, 'imagem': imagem})


@permission_required('imagens.delete_imagem', raise_exception=True)
def excluir_imagem(request, id):
    imagem = get_object_or_404(Imagem, pk=id)

    if request.method == 'POST':
        imagem.delete()
        messages.success(request, 'Imagem excluida com sucesso!')
        return redirect('listar_imagens')

    return render(request, 'imagens/excluir.html', {'imagem': imagem})
