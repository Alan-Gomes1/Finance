from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Perfil.as_view(), name='home'),
]
