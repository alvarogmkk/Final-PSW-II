from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from decimal import Decimal, ROUND_HALF_UP

from pagamento.models import Pagamento
from usuario.models import Usuario

from .forms import ReservaForm
from .models import Reserva


@login_required
def criar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST, usuario=request.user)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.fk_usuario = get_object_or_404(Usuario, pk=request.user.pk)
            salvar_reserva_com_pagamento(reserva, form.cleaned_data['metodo_pagamento'])

            messages.success(request, 'Reserva criada com sucesso!')
            return redirect('listar_reservas')
    else:
        initial = {}
        locacao_id = request.GET.get('locacao')
        if locacao_id:
            initial['fk_locacao'] = locacao_id

        form = ReservaForm(initial=initial, usuario=request.user)

    return render(request, 'reservas/criar.html', {'form': form})


@login_required
def listar_reservas(request):
    if request.user.is_staff:
        reservas = Reserva.objects.select_related('fk_usuario', 'fk_locacao', 'fk_pagamento').all()
    else:
        usuario = get_object_or_404(Usuario, pk=request.user.pk)
        reservas = Reserva.objects.select_related(
            'fk_usuario',
            'fk_locacao',
            'fk_pagamento',
        ).filter(fk_usuario=usuario)

    return render(request, 'reservas/listar.html', {'reservas': reservas})


@login_required
def detalhar_reserva(request, id):
    reserva = get_object_or_404(
        Reserva.objects.select_related('fk_usuario', 'fk_locacao', 'fk_pagamento'),
        pk=id,
    )

    if not request.user.is_staff and reserva.fk_usuario.pk != request.user.pk:
        return HttpResponseForbidden('Você não tem permissão para acessar esta reserva.')

    return render(request, 'reservas/detalhar.html', {'reserva': reserva})


@login_required
def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, pk=id)

    if not request.user.is_staff and reserva.fk_usuario.pk != request.user.pk:
        return HttpResponseForbidden('Você não tem permissão para editar esta reserva.')

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva, usuario=request.user)
        if form.is_valid():
            reserva = form.save(commit=False)
            salvar_reserva_com_pagamento(reserva, form.cleaned_data['metodo_pagamento'])
            messages.success(request, 'Reserva atualizada com sucesso!')
            return redirect('detalhar_reserva', id=reserva.id)
    else:
        form = ReservaForm(instance=reserva, usuario=request.user)

    return render(request, 'reservas/editar.html', {'form': form, 'reserva': reserva})


@login_required
def excluir_reserva(request, id):
    reserva = get_object_or_404(Reserva, pk=id)

    if not request.user.is_staff and reserva.fk_usuario.pk != request.user.pk:
        return HttpResponseForbidden('Você não tem permissão para excluir esta reserva.')

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva excluida com sucesso!')
        return redirect('listar_reservas')

    return render(request, 'reservas/excluir.html', {'reserva': reserva})

def preencher_valor_total(reserva):
    dias = (reserva.data_saida - reserva.data_entrada).days
    reserva.valor_total = (Decimal(str(reserva.fk_locacao.preco_diaria)) * dias).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


@transaction.atomic
def salvar_reserva_com_pagamento(reserva, metodo):
    preencher_valor_total(reserva)
    pagamento = reserva.fk_pagamento
    if pagamento is None:
        pagamento = Pagamento(status='pendente')
    pagamento.valor = reserva.valor_total
    pagamento.metodo = metodo or pagamento.metodo or 'pix'
    pagamento.save()
    reserva.fk_pagamento = pagamento
    reserva.save()
