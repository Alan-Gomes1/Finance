from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Perfil.as_view(), name='home'),
    path('gerenciar/', views.Gerenciar.as_view(), name='gerenciar'),
    path('cadastrar_banco/', views.CadastrarBanco.as_view(),
         name='cadastrar_banco'),
    path('cadastrar_categoria/', views.CadastrarCategoria.as_view(),
         name='cadastrar_categoria'),
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path('deletar_banco/<int:pk>', views.DeletarBanco.as_view(),
         name='deletar_banco'),
    path('update_categoria/<int:id>', views.UpdateCategoria.as_view(),
         name='update_categoria'),
]
