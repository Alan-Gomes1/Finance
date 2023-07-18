from django.urls import path
from . import views

urlpatterns = [
    path('definir_planejamento/', views.DefinirPlanejamento.as_view(),
         name='definir_planejamento'),
    path('update_valor_categoria/<int:id>/',
         views.UpdateValorCategoria.as_view(), name='update_valor_categoria'),
    path('ver_planejamento/', views.VerPlanejamento.as_view(),
         name='ver_planejamento'),
]
