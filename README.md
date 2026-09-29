# Final-PSW-II

## Catálogo ACasa com o template Haus

A interface usa o visual do Haus fornecido em `haus/haus`, adaptado aos
templates Django. Os estilos utilizados estão em `Acasa/static/haus/css` e
`Acasa/static/css/style.css`; o menu móvel usa `Acasa/static/js/site.js`.
O template original foi preservado. Crédito do design: uiCookies.

O catálogo tem busca por nome, descrição, cidade e endereço; filtros por
categoria, aluguel mensal máximo, quartos e disponibilidade; ordenação e
paginação. Os novos campos são opcionais para preservar imóveis antigos.
**O preço mensal é informativo. As reservas existentes continuam por diária.**

Na pasta `Acasa`, prepare o banco com:

```powershell
python manage.py migrate
python manage.py popular_demo
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` ou `/locacoes/`. O comando `popular_demo`
adiciona 10 imóveis fictícios, com duas fotos cada, sem usar IDs fixos nem
sobrescrever registros existentes. Pode ser repetido sem duplicar os imóveis
de demonstração identificados pelo nome. Alterações feitas nesses registros
são preservadas. Prefira esse comando a carregar a fixture diretamente.

Os imóveis demonstrativos têm aluguel mensal de R$ 950 a R$ 9.800, de 28 a
320 m², e estão identificados como fictícios. Fotos ilustrativas originadas
nas URLs Unsplash da fixture foram incluídas em `Acasa/static/imoveis`.
`Imagem.url` mantém a URL original editável; `url_exibicao` utiliza a cópia
local quando disponível. O site não precisa acessar a rede para essas fotos.

Login, cadastro, categorias, imagens, pagamentos, usuários e reservas
continuam nas rotas existentes. A administração Django permanece em `/admin/`,
com as credenciais administrativas já cadastradas; a carga de demonstração
não cria nem altera contas ou senhas.

Antes da migração desta integração, uma cópia local do SQLite foi criada em
`.local/backups/`. Essa pasta e as ferramentas locais de verificação não são
versionadas. Não publique bancos ou backups contendo dados pessoais.

Execute os testes **a partir da pasta `Acasa`**:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Os testes verificam os dados demonstrativos, repetição da carga, busca,
filtros combinados e inválidos, ordenação, paginação, detalhes e imagens,
cadastro/edição/exclusão de imóvel, compatibilidade dos imóveis antigos,
reserva por diária, bloqueio de imóvel indisponível, login e permissões.

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
