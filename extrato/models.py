from django.db import models

from contas.abstracts import BaseModel
from perfil.models import Categoria, Conta


class Valores(BaseModel):
    tipos = (
        ('E', 'Entrada'),
        ('S', 'Saída')
    )

    valor = models.FloatField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    data = models.DateField()
    tipo = models.CharField(max_length=1, choices=tipos)

    def __str__(self):
        return self.descricao
