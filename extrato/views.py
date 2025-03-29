import os
from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View

import pdfkit

from perfil.models import Categoria, Conta

from .models import Valores


class NovoValor(View):
    def get(self, request):
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()

        return render(
            request, "novo_valor.html",
            {"contas": contas, "categorias": categorias}
        )

    def post(self, request):
        valor = request.POST.get("valor")
        categoria_id = request.POST.get("categoria")
        descricao = request.POST.get("descricao")
        data = request.POST.get("data")
        conta_id = request.POST.get("conta")
        tipo = request.POST.get("tipo")

        valores = Valores(
            valor=valor,
            categoria_id=categoria_id,
            descricao=descricao,
            data=data,
            conta_id=conta_id,
            tipo=tipo,
        )
        valores.save()

        conta = Conta.objects.get(id=conta_id)
        if tipo == "E":
            conta.valor += int(valor)
        else:
            conta.valor -= int(valor)
        conta.save()

        messages.add_message(
            request, constants.SUCCESS, "Valor cadastrado com sucesso"
        )
        return redirect("novo_valor")


class ViewExtrato(View):
    def get(self, request):
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        valores = Valores.objects.filter(data__month=datetime.now().month)

        conta_id = request.GET.get("conta")
        categoria_id = request.GET.get("categoria")

        if conta_id:
            valores = valores.filter(conta__id=conta_id)

        if categoria_id:
            valores = valores.filter(categoria__id=categoria_id)

        return render(
            request, "view_extrato.html",
            {"contas": contas, "categorias": categorias, "valores": valores}
        )


class ExportarPDF(View):
    def get(self, request):
        valores = Valores.objects.filter(data__month=datetime.now().month)
        camino_template = os.path.join(
            settings.BASE_DIR, 'templates/parcial/extrato.html'
        )
        template = render_to_string(camino_template, {"valores": valores})

        path_output = BytesIO()
        pdfkit.from_string(template, path_output)
        # HTML(string=template).write_pdf(path_output)
        path_output.seek(0)

        return FileResponse(path_output, filename="extrato.pdf")
