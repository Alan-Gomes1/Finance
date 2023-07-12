from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Perfil.as_view(), name='home'),
    path('gerenciar/', views.Gerenciar.as_view(), name='gerenciar'),
    path(
        'cadastrar_banco', views.CadastrarBanco.as_view(),
        name='cadastrar_banco'
    ),
]
