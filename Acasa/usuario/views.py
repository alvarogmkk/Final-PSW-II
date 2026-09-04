from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import CadastroForm, UsuarioForm
from .models import Usuario


@permission_required('usuario.view_usuario', raise_exception=True)
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar.html', {'usuarios': usuarios})


@permission_required('usuario.add_usuario', raise_exception=True)
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario criado com sucesso!')
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/criar.html', {'form': form})


@login_required
def detalhar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    if not request.user.is_staff and usuario.pk != request.user.pk:
        return HttpResponseForbidden('Você não tem permissão para acessar este usuário.')
    return render(request, 'usuarios/detalhar.html', {'usuario': usuario})


@login_required
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    if not request.user.is_staff and usuario.pk != request.user.pk:
        return HttpResponseForbidden('Você não tem permissão para editar este usuário.')

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario atualizado com sucesso!')
            return redirect('detalhar_usuario', id=usuario.id)
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/editar.html', {'form': form, 'usuario': usuario})


@permission_required('usuario.delete_usuario', raise_exception=True)
def excluir_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario excluido com sucesso!')
        return redirect('listar_usuarios')

    return render(request, 'usuarios/excluir.html', {'usuario': usuario})


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
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('home')

        messages.error(request, 'Usuario ou senha invalidos.')

    return render(request, 'usuarios/login.html')


@require_POST
@login_required
def logout_usuario(request):
    logout(request)
    messages.success(request, 'Voce saiu do sistema.')
    return redirect('home')
