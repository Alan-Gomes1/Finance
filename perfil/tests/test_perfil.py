from django.urls import reverse

from perfil.models import Conta
from perfil.tests.conftest import BaseTestCase


class TestProfile(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('home')

    def test_profile_view_loads_home_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')

    def test_profile_view_returns_status_code_200_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_does_not_accept_post_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_profile_view_url_is_correct(self):
        self.assertEqual(self.url, '/perfil/home/')


class TestManage(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('gerenciar')

    def test_manage_view_loads_manage_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'gerenciar.html')

    def test_manage_view_returns_status_code_200_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_manage_view_does_not_accept_post_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_manage_view_url_is_correct(self):
        self.assertEqual(self.url, '/perfil/gerenciar/')


class TestRegisterBank(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('cadastrar_banco')

    def dados_banco(self):
        return {
            'nome': 'Bank Name',
            'banco': 'Bank XYZ',
            'tipo': 'Type A',
            'valor': 1000,
        }

    def test_register_bank_successfully(self):
        data = self.dados_banco()
        self.client.post(self.url, data)
        account = Conta.objects.first()
        self.assertEqual(
            account, Conta.objects.filter(nome='Bank Name').first()
        )

    def test_register_bank_view_returns_status_code_302_redirect(self):
        data = self.dados_banco()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

    def test_register_bank_view_does_not_accept_get_request(self):
        data = self.dados_banco()
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 405)

    def test_register_bank_view_success_message(self):
        data = self.dados_banco()
        response = self.client.post(self.url, data)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(messages[0].message, 'Conta cadastrada com sucesso')

    def test_register_bank_view_error_message(self):
        data = {
            'nome': '     ',
            'banco': '    ',
            'tipo': '',
            'valor': ''
        }
        response = self.client.post(self.url, data)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(messages[0].message, 'Preencha todos os campos')

    def test_register_bank_view_url_is_correct(self):
        self.assertEqual(self.url, '/perfil/cadastrar_banco/')


class TestDeleteBank(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.account = Conta.objects.create(nome="Test Account", valor=150)
        self.url = reverse('deletar_banco', kwargs={"pk": self.account.pk})
        self.response = self.client.get(self.url)

    def test_delete_bank_view_successfully(self):
        message = list(self.response.wsgi_request._messages)
        self.assertEqual(
            message[0].message, "Conta deletada com sucesso"
        )

    def test_delete_bank_view_url_is_correct(self):
        self.assertEqual(self.url, '/perfil/deletar_banco/1')

    def test_delete_bank_view_redirects_to_manage(self):
        self.assertRedirects(self.response, reverse("gerenciar"))

    def test_delete_bank_view_returns_status_code_302_redirect(self):
        self.assertEqual(self.response.status_code, 302)

    def test_delete_bank_view_existing_account_is_deleted(self):
        pk = self.account.pk
        self.account.delete()
        with self.assertRaises(Conta.DoesNotExist):
            Conta.objects.get(pk=pk)
