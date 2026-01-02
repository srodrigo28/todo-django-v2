from django.contrib import admin
from .models import Tarefa

# Exemplo 1 
# # admin.site.register(Tarefa)

# Exemplo 2
@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'finalizado', 'criado_em')
    search_fields = ('titulo',)

