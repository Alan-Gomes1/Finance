from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from perfil.models import Categoria

from .models import ContaPagar, ContaPaga


class DefinirContas(View):
    def get(self, request):
        categorias = Categoria.objects.all()
        return render(
            request, 'definir_contas.html', {'categorias': categorias}
        )

    def post(self, request):
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = ContaPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento
        )
        conta.save()

        messages.success(request, 'Conta cadastrada com sucesso')
        return redirect('definir_contas')


class VerContas(View):
    def get(self, request):
        MES_ATUAL = datetime.now().month
        DIA_ATUAL = datetime.now().day

        contas = ContaPagar.objects.all()
        contas_pagas = ContaPaga.objects.filter(
            data_pagamento__month=MES_ATUAL
        ).values('conta')

        contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(
            id__in=contas_pagas
        )
        contas_proximas_vencimento = contas.filter(
            dia_pagamento__lte=DIA_ATUAL + 7
        ).filter(dia_pagamento__gt=DIA_ATUAL).exclude(id__in=contas_pagas)

        restantes = contas.exclude(id__in=contas_pagas).exclude(
            id__in=contas_vencidas
        ).exclude(id__in=contas_proximas_vencimento)

        return render(
            request, 'ver_contas.html',
            {'contas': contas, 'contas_vencidas': contas_vencidas,
             'contas_proximas_vencimento': contas_proximas_vencimento,
             'restantes': restantes}
        )
