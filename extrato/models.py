from django.db import models

from perfil.models import Categoria, Conta


class Valores(models.Model):
    tipos = (
        ('E', 'Entrada'),
        ('S', 'Saída')
    )

    valor = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    data = models.DateField()
    tipo = models.CharField(max_length=1, choices=tipos)

    def __str__(self):
        return self.descricao
