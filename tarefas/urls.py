from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Tela Inicial (Cadastro)
    path('', views.cadastrar_usuario, name='cadastrar_usuario'),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # App
    path('tarefas/', views.listar_tarefas, name='listar_tarefas'),
    path('nova/', views.nova_tarefa, name='nova_tarefa'),
    path('editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    path('tarefa/<int:tarefa_id>/', views.detalhes_tarefa, name='detalhes_tarefa'),
    path('deletar/<int:tarefa_id>/', views.deletar_tarefa, name='deletar_tarefa'),
]