from django.urls import path
from . import views

urlpatterns = [
    path('definir_contas', views.DefinirContas.as_view(),
         name='definir_contas'),
    path('ver_contas', views.VerContas.as_view(),
         name='ver_contas'),
]
