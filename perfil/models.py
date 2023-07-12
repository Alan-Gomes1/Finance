from django.db import models


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

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

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=bancos)
    tipo = models.CharField(max_length=2, choices=tipo)
    valor = models.FloatField()
    icone = models.ImageField(upload_to="icones")

    def __str__(self) -> str:
        return self.apelido
