from django.urls import path
from . import views

urlpatterns = [
    path('novo_valor/', views.NovoValor.as_view(), name='novo_valor'),
    path('view_extrato/', views.ViewExtrato.as_view(), name='view_extrato'),
]
