from datetime import datetime

from django.db import models
from django.db.models import Sum


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(
            categoria__id=self.id
        ).filter(data__month=datetime.now().month).filter(
            tipo='S'
        ).aggregate(total=Sum('valor'))
        return valores['total'] if valores['total'] else 0

    def percentual_gasto_por_categoria(self):
        try:
            return int((self.total_gasto() * 100) / self.valor_planejamento)
        except:
            return 0

    def __str__(self) -> str:
        return self.categoria


class Conta(models.Model):
    bancos = (
        ("NU", "Nubank"),
        ("BR", "Bradesco"),
        ("BB", "Banco do Brasil"),
        ("IT", "Itau"),
        ("SE", "Santander"),
        ("CE", "Caixa Economica"),
    )

    tipo = (
        ("pf", "Pessoa física"),
        ("pj", "Pessoa jurídica"),
    )

    nome = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=bancos)
    tipo = models.CharField(max_length=2, choices=tipo)
    valor = models.FloatField()
    icone = models.ImageField(upload_to="icones")

    def __str__(self) -> str:
        return self.nome
