from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, Prefetch, Q
from django.core.paginator import Paginator
from imagens.models import Imagem

from categoria.models import Categoria

from .forms import BuscaLocacaoForm, LocacaoForm
from .models import Locacao


def catalogo():
    return Locacao.objects.select_related('fk_categoria').prefetch_related(
        Prefetch('imagens', queryset=Imagem.objects.order_by('-principal', 'ordem', 'pk'))
    ).order_by('-pk')


def home(request):
    locacoes = catalogo().filter(disponivel=True)
    return render(request, 'home/home.html', {
        'locacoes': locacoes[:6], 'total_imoveis': locacoes.count(),
        'categorias': Categoria.objects.order_by('nome'), 'filtros': BuscaLocacaoForm(),
    })


def listar_locacoes(request):
    locacoes = catalogo()
    filtros = BuscaLocacaoForm(request.GET)
    if filtros.is_valid():
        dados = filtros.cleaned_data
        if dados['q']:
            locacoes = locacoes.filter(Q(nome__icontains=dados['q']) | Q(local__icontains=dados['q']) | Q(endereco__icontains=dados['q']) | Q(descricao__icontains=dados['q']))
        if dados['categoria']:
            locacoes = locacoes.filter(fk_categoria=dados['categoria'])
        if dados['preco_max'] is not None:
            locacoes = locacoes.filter(preco_mensal__lte=dados['preco_max'])
        if dados['quartos'] is not None:
            locacoes = locacoes.filter(quartos__gte=dados['quartos'])
        if dados['status']:
            locacoes = locacoes.filter(disponivel=dados['status'] == 'disponivel')
        ordenacao = {'menor_preco': F('preco_mensal').asc(nulls_last=True),
                     'maior_preco': F('preco_mensal').desc(nulls_last=True),
                     'area': F('area_m2').desc(nulls_last=True)}
        if dados['ordenar'] in ordenacao:
            locacoes = locacoes.order_by(ordenacao[dados['ordenar']], '-pk')
    else:
        locacoes = locacoes.none()
    pagina = Paginator(locacoes, 12).get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    return render(request, 'locacoes/listar.html', {'locacoes': pagina, 'page_obj': pagina,
                  'filtros': filtros, 'parametros': parametros.urlencode()})


def detalhar_locacao(request, id):
    locacao = get_object_or_404(catalogo(), pk=id)
    imagens = locacao.imagens.all()
    return render(request, 'locacoes/detalhar.html', {'locacao': locacao, 'imagens': imagens})


@permission_required('locacao.add_locacao', raise_exception=True)
def criar_locacao(request):
    if request.method == 'POST':
        form = LocacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Locacao cadastrada com sucesso!')
            return redirect('listar_locacoes')
    else:
        form = LocacaoForm()

    return render(request, 'locacoes/criar.html', {'form': form})



@permission_required('locacao.change_locacao', raise_exception=True)
def editar_locacao(request, id):
    locacao = get_object_or_404(Locacao, pk=id)

    if request.method == 'POST':
        form = LocacaoForm(request.POST, instance=locacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Locacao atualizada com sucesso!')
            return redirect('detalhar_locacao', id=locacao.id)
    else:
        form = LocacaoForm(instance=locacao)

    return render(request, 'locacoes/editar.html', {'form': form, 'locacao': locacao})



@permission_required('locacao.delete_locacao', raise_exception=True)
def excluir_locacao(request, id):
    locacao = get_object_or_404(Locacao, pk=id)

    if request.method == 'POST':
        locacao.delete()
        messages.success(request, 'Locacao excluida com sucesso!')
        return redirect('listar_locacoes')

    return render(request, 'locacoes/excluir.html', {'locacao': locacao})
