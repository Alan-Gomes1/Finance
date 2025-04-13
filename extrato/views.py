import os
from datetime import datetime
from io import BytesIO

import pdfkit
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View
from finance.logger import logger

from perfil.models import Categoria, Conta
from .models import Valores
from .tasks import send_email_task


class NovoValor(LoginRequiredMixin, View):
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


class ViewExtrato(LoginRequiredMixin, View):
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


class ExportarPDF(LoginRequiredMixin, View):
    def get(self, request):
        valores = Valores.objects.filter(data__month=datetime.now().month)
        camino_template = os.path.join(
            settings.BASE_DIR, 'templates/parcial/extrato.html'
        )
        template = render_to_string(camino_template, {"valores": valores})
        options = {"enable-local-file-access": "", "encoding": "UTF-8"}
        pdf_buffer = BytesIO()
        pdf_buffer.write(pdfkit.from_string(template, False, options=options))
        pdf_buffer.seek(0)

        send_email_task.delay(
            subject="Extrato",
            message="Seu extrato foi exportado como pdf com sucesso!",
            recipient_list=[request.user.email],
        )
        logger.info("Extrato exportado com sucesso!")

        return FileResponse(pdf_buffer, filename="extrato.pdf")
