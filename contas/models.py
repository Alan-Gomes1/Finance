from django.db import models

from .abstracts import BaseModel
from perfil.models import Categoria


class ContaPagar(BaseModel):
    titulo = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    valor = models.FloatField()
    dia_pagamento = models.IntegerField()

    def __str__(self):
        return self.titulo


class ContaPaga(BaseModel):
    conta = models.ForeignKey(ContaPagar, on_delete=models.DO_NOTHING)
    data_pagamento = models.DateField()
