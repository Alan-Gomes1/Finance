from datetime import datetime

from django.urls import reverse

from .models import Valores
from perfil.models import Conta, Categoria
from perfil.tests.conftest import BaseTestCase


class ViewExtractTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("view_extrato")
        self.account = Conta.objects.create(nome="Conta Teste", valor=1000)
        self.category = Categoria.objects.create(
            categoria="Categoria Teste", essencial=True, valor_planejamento=500
        )
        self.value = Valores.objects.create(
            valor=200,
            categoria=self.category,
            descricao="Teste de valor",
            data=datetime.now(),
            conta=self.account,
            tipo="E",
        )

    def test_extract_view_returns_status_code_200_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_extract_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "view_extrato.html")

    def test_extract_view_filter_by_account(self):
        response = self.client.get(self.url, {"conta": self.account.id})
        self.assertContains(response, self.account.nome)
        valores_in_context = response.context['valores']
        self.assertTrue(
            all(v.conta == self.account for v in valores_in_context)
        )

    def test_extract_view_filter_by_category(self):
        response = self.client.get(
            self.url, {"categoria": self.category.id}
        )
        self.assertContains(response, self.category.categoria)
        valores_in_context = response.context['valores']
        self.assertTrue(
            all(v.categoria == self.category for v in valores_in_context)
        )
