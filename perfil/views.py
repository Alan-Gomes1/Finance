from datetime import datetime
from typing import Any, Dict

from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from extrato.models import Valores

from .models import Categoria, Conta
from .utils import calcula_total, calcula_equilibrio_financeiro


class ListViewBase(ListView):
    model = Conta
    context_object_name = "contas"
    total = calcula_total(Conta.objects.all())
    valores = Valores.objects.filter(
        data__month=datetime.now().month
    )
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')
    total_essenciais, total_nao_essenciais = calcula_equilibrio_financeiro()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        contexto = super().get_context_data(**kwargs)
        contexto["total"] = self.total
        contexto["categorias"] = Categoria.objects.all()
        contexto['total_entradas'] = calcula_total(self.entradas)
        contexto['total_saidas'] = calcula_total(self.saidas)
        contexto['total_gastos_essenciais'] = int(self.total_essenciais)
        contexto['total_gastos_nao_essenciais'] = int(self.total_nao_essenciais)  # noqa: E501
        return contexto


class Perfil(ListViewBase):
    template_name = "home.html"


class Gerenciar(ListViewBase):
    template_name = "gerenciar.html"


class CadastrarBanco(View):
    def post(self, request):
        nome = request.POST.get("nome")
        banco = request.POST.get("banco")
        tipo = request.POST.get("tipo")
        valor = request.POST.get("valor")
        icone = request.FILES.get("icone")

        if len(nome.strip()) == 0 or len(valor.strip()) == 0:
            messages.add_message(
                request, constants.ERROR, "Preencha todos os campos"
            )
            return redirect(reverse("gerenciar"))

        conta = Conta(
            nome=nome,
            banco=banco,
            tipo=tipo,
            valor=valor,
            icone=icone
        )
        conta.save()

        messages.add_message(
            request, constants.SUCCESS, "Conta cadastrada com sucesso"
        )
        return redirect(reverse("gerenciar"))


class DeletarBanco(View):
    def get(self, request, pk):
        conta = get_object_or_404(Conta, id=pk)
        conta.delete()
        messages.add_message(
            request, constants.SUCCESS, "Conta deletada com sucesso"
        )
        return redirect(reverse("gerenciar"))


class CadastrarCategoria(View):
    def post(self, request):
        nome = request.POST.get("categoria")
        essencial = bool(request.POST.get("essencial"))

        categoria = Categoria(
            categoria=nome,
            essencial=essencial
        )
        categoria.save()

        messages.add_message(
            request, constants.SUCCESS, "Categoria cadastrada com sucesso"
        )
        return redirect(reverse("gerenciar"))


class UpdateCategoria(View):
    def get(self, request, id):
        categoria = get_object_or_404(Categoria, id=id)
        categoria.essencial = not categoria.essencial
        categoria.save()
        return redirect(reverse("gerenciar"))


class Dashboard(View):
    def get(self, request):
        dados = {}
        categorias = Categoria.objects.all()

        for categoria in categorias:
            dados[categoria.categoria] = Valores.objects.filter(
                categoria=categoria
            ).aggregate(total=Coalesce(Sum("valor"), 0.0))['total']

        return render(
            request, "dashboard.html",
            {"labels": list(dados.keys()), "values": list(dados.values())}
        )
