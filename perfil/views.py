from typing import Any, Dict

from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .models import Categoria, Conta
from .utils import calcula_total


class ListViewBase(ListView):
    model = Conta
    context_object_name = "contas"
    total = calcula_total(Conta.objects.all(), "valor")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        contexto = super().get_context_data(**kwargs)
        contexto["total"] = self.total
        contexto["categorias"] = Categoria.objects.all()
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
    def get(self, request, id):
        conta = get_object_or_404(Conta, id=id)
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
