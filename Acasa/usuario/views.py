from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import CadastroForm


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
