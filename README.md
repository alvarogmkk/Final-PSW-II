# Final-PSW-II

## Autenticação e permissões

O projeto utiliza `django.contrib.auth`, incluindo sessões, middleware de
autenticação, formulário de cadastro com senha criptografada e fluxo de
login/logout. As rotas são protegidas por decorators:

- `@login_required`: reservas, perfil e logout;
- `@permission_required`: inclusão, alteração e remoção de locações,
  categorias, imagens e pagamentos;
- `@permission_required`: administração de usuários, locações, categorias,
  imagens e pagamentos.

Usuários comuns somente acessam e administram as próprias reservas. Crie um
superusuário para a administração completa; para perfis administrativos menos
amplos, crie grupos e atribua as permissões dos modelos no `/admin/`.

### Execução local

No Windows deste projeto, o Python está instalado em
`C:\Users\alvar\AppData\Local\Programs\Python\Python313\python.exe`, mas
não está configurado no `PATH`. No PowerShell, entre na pasta `Acasa` e crie
um ambiente virtual com:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r ..\requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Execute a verificação e os testes com:

```powershell
python manage.py check
python manage.py test
```
