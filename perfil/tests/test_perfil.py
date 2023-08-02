from django.test import TestCase
from django.urls import reverse


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
