from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    # Relaciona 1 Perfil para 1 Usuário
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='perfis/', default='default.png', blank=True)
    telefone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

class Tarefa(models.Model):
    # Relaciona a tarefa ao usuário logado
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    finalizado = models.BooleanField(default=False)
    
    # Campo para "esconder" a tarefa sem apagar do banco
    excluida = models.BooleanField(default=False)
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo