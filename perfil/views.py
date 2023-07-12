from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render  # noqa
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from .models import Conta


class Perfil(TemplateView):
    template_name = "home.html"


class Gerenciar(TemplateView):
    template_name = "gerenciar.html"


class CadastrarBanco(View):
    def post(self, request):
        apelido = request.POST.get("apelido")
        banco = request.POST.get("banco")
        tipo = request.POST.get("tipo")
        valor = request.POST.get("valor")
        icone = request.FILES.get("icone")

        if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
            messages.add_message(
                request, constants.ERROR, "Preencha todos os campos"
            )
            return redirect(reverse("gerenciar"))

        conta = Conta(
            apelido=apelido,
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
