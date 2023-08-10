from django.test import TestCase
from django.urls import reverse

from perfil.models import Conta


class TestPerfil(TestCase):
    def test_view_perfil_carrega_template_home(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_view_perfil_retorna_status_code_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_perfil_nao_aceita_requisicao_post(self):
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 405)

    def test_view_perfil_url_esta_correta(self):
        url = reverse('home')
        self.assertEqual(url, '/perfil/home/')


class TestGerenciar(TestCase):
    def test_view_gerenciar_carrega_template_correto(self):
        response = self.client.get(reverse('gerenciar'))
        self.assertTemplateUsed(response, 'gerenciar.html')

    def test_view_gerenciar_retorna_status_code_200(self):
        response = self.client.get(reverse('gerenciar'))
        self.assertEqual(response.status_code, 200)

    def test_view_gerenciar_nao_aceita_requisicao_post(self):
        response = self.client.post(reverse('gerenciar'))
        self.assertEqual(response.status_code, 405)

    def test_view_gerenciar_url_esta_correta(self):
        url = reverse('gerenciar')
        self.assertEqual(url, '/perfil/gerenciar/')


class TestCadastrarBanco(TestCase):
    def dados_banco(self):
        return {
            'nome': 'Nome do Banco',
            'banco': 'Banco XYZ',
            'tipo': 'Tipo A',
            'valor': 1000,
        }

    def test_view_CadastrarBanco_com_sucesso(self):
        dados = self.dados_banco()
        self.client.post(reverse('cadastrar_banco'), dados)
        conta = Conta.objects.first()
        self.assertEqual(
            conta, Conta.objects.filter(nome='Nome do Banco').first()
        )

    def test_view_CadastrarBanco_retorna_status_code_302(self):
        dados = self.dados_banco()
        response = self.client.post(reverse('cadastrar_banco'), dados)
        self.assertEqual(response.status_code, 302)

    def test_view_CadastratBanco_nao_aceita_requisicao_get(self):
        dados = self.dados_banco()
        response = self.client.get(reverse('cadastrar_banco'), dados)
        self.assertEqual(response.status_code, 405)

    def test_view_CadastrarBanco_mensagem_de_sucesso(self):
        dados = self.dados_banco()
        response = self.client.post(reverse('cadastrar_banco'), dados)
        mensagens = list(response.wsgi_request._messages)
        self.assertEqual(mensagens[0].message, 'Conta cadastrada com sucesso')

    def test_view_CadastrarBanco_mensagem_de_erro(self):
        dados = {
            'nome': '     ',
            'banco': '    ',
            'tipo': '',
            'valor': ''
        }
        response = self.client.post(reverse('cadastrar_banco'), dados)
        mensagens = list(response.wsgi_request._messages)
        self.assertEqual(mensagens[0].message, 'Preencha todos os campos')

    def test_view_CadastrarBanco_url_esta_correta(self):
        url = reverse('cadastrar_banco')
        self.assertEqual(url, '/perfil/cadastrar_banco/')
