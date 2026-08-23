from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CadastroForm, CategoriaForm, LocacaoForm, ReservaForm
from .models import Categoria, Locacao, Pagamento, Reserva, Usuario


def home(request):
    locacoes = Locacao.objects.select_related('fk_categoria').all()[:6]
    categorias = Categoria.objects.all()[:6]
    return render(request, 'home/home.html', {'locacoes': locacoes, 'categorias': categorias})


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
            messages.success(request, 'Locação cadastrada com sucesso!')
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
            messages.success(request, 'Locação atualizada com sucesso!')
            return redirect('detalhar_locacao', id=locacao.id)
    else:
        form = LocacaoForm(instance=locacao)

    return render(request, 'locacoes/editar.html', {'form': form, 'locacao': locacao})


@login_required
def excluir_locacao(request, id):
    locacao = get_object_or_404(Locacao, pk=id)

    if request.method == 'POST':
        locacao.delete()
        messages.success(request, 'Locação excluída com sucesso!')
        return redirect('listar_locacoes')

    return render(request, 'locacoes/excluir.html', {'locacao': locacao})


def cadastro_usuario(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login_usuario')
    else:
        form = CadastroForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')

        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'usuarios/login.html')


def logout_usuario(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema.')
    return redirect('home')


@login_required
def criar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            usuario, _ = Usuario.objects.get_or_create(fk_user=request.user)
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
        reservas = Reserva.objects.select_related('fk_usuario__fk_user', 'fk_locacao', 'fk_pagamento').all()
    else:
        usuario = get_object_or_404(Usuario, fk_user=request.user)
        reservas = Reserva.objects.select_related('fk_usuario__fk_user', 'fk_locacao', 'fk_pagamento').filter(fk_usuario=usuario)

    return render(request, 'reservas/listar.html', {'reservas': reservas})


@login_required
def detalhar_reserva(request, id):
    reserva = get_object_or_404(Reserva.objects.select_related('fk_usuario__fk_user', 'fk_locacao', 'fk_pagamento'), pk=id)

    if not request.user.is_staff and reserva.fk_usuario.fk_user != request.user:
        messages.error(request, 'Você não tem permissão para acessar esta reserva.')
        return redirect('listar_reservas')

    return render(request, 'reservas/detalhar.html', {'reserva': reserva})
