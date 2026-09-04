from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PagamentoForm
from .models import Pagamento


@permission_required('pagamento.view_pagamento', raise_exception=True)
def listar_pagamentos(request):
    pagamentos = Pagamento.objects.all()
    return render(request, 'pagamentos/listar.html', {'pagamentos': pagamentos})


@permission_required('pagamento.view_pagamento', raise_exception=True)
def detalhar_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, pk=id)
    return render(request, 'pagamentos/detalhar.html', {'pagamento': pagamento})


@permission_required('pagamento.add_pagamento', raise_exception=True)
def criar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento cadastrado com sucesso!')
            return redirect('listar_pagamentos')
    else:
        form = PagamentoForm()

    return render(request, 'pagamentos/criar.html', {'form': form})


@permission_required('pagamento.change_pagamento', raise_exception=True)
def editar_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, pk=id)

    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso!')
            return redirect('detalhar_pagamento', id=pagamento.id)
    else:
        form = PagamentoForm(instance=pagamento)

    return render(request, 'pagamentos/editar.html', {'form': form, 'pagamento': pagamento})


@permission_required('pagamento.delete_pagamento', raise_exception=True)
def excluir_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, pk=id)

    if request.method == 'POST':
        pagamento.delete()
        messages.success(request, 'Pagamento excluido com sucesso!')
        return redirect('listar_pagamentos')

    return render(request, 'pagamentos/excluir.html', {'pagamento': pagamento})
