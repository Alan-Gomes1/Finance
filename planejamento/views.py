from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from perfil.models import Categoria


class DefinirPlanejamento(View, LoginRequiredMixin):
    def get(self, request):
        categorias = Categoria.objects.all()
        return render(
            request, 'definir_planejamento.html', {'categorias': categorias}
        )


class UpdateValorCategoria(View, LoginRequiredMixin):
    def post(self, request, id):
        novo_valor = request.POST.get('valor')
        categoria = get_object_or_404(Categoria, id=id)
        categoria.valor_planejamento = novo_valor
        categoria.save()

        return redirect('definir_planejamento')


class VerPlanejamento(View, LoginRequiredMixin):
    def get(self, request):
        categorias = Categoria.objects.all()
        return render(
            request, 'ver_planejamento.html', {'categorias': categorias}
        )
