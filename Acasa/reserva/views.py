from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from pagamento.models import Pagamento
from usuario.models import Usuario

from .forms import ReservaForm
from .models import Reserva


@login_required
def criar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            usuario = get_object_or_404(Usuario, pk=request.user.pk)
            dados = form.cleaned_data
            dias = (dados['data_saida'] - dados['data_entrada']).days
            valor_total = dias * dados['fk_locacao'].preco_diaria

            pagamento = Pagamento.objects.create(
                valor=valor_total,
                status='pendente',
                metodo='pix',
            )

            reserva = form.save(commit=False)
            reserva.fk_usuario = usuario
            reserva.valor_total = valor_total
            reserva.status = 'pendente'
            reserva.fk_pagamento = pagamento
            reserva.save()

            messages.success(request, 'Reserva criada com sucesso!')
            return redirect('listar_reservas')
    else:
        form = ReservaForm()

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
        messages.error(request, 'Voce nao tem permissao para acessar esta reserva.')
        return redirect('listar_reservas')

    return render(request, 'reservas/detalhar.html', {'reserva': reserva})
