from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CadastroForm, UsuarioForm
from .models import Usuario


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar.html', {'usuarios': usuarios})


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


def detalhar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    return render(request, 'usuarios/detalhar.html', {'usuario': usuario})


def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario atualizado com sucesso!')
            return redirect('detalhar_usuario', id=usuario.id)
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/editar.html', {'form': form, 'usuario': usuario})


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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')

        messages.error(request, 'Usuario ou senha invalidos.')

    return render(request, 'usuarios/login.html')


def logout_usuario(request):
    logout(request)
    messages.success(request, 'Voce saiu do sistema.')
    return redirect('home')
