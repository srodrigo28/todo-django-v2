from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tarefa, Perfil
from .forms import CadastroForm

# --- VIEW DE CADASTRO (PÚBLICA) ---
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            # 1. Cria o objeto mas não salva no banco ainda
            user = form.save(commit=False)
            
            # 2. O PULO DO GATO: Pega o email e joga no username
            email_digitado = form.cleaned_data.get('email')
            user.username = email_digitado 
            
            # 3. Salva o usuário oficialmente
            user.save()

            # 4. Cria o perfil vinculado (Telefone)
            Perfil.objects.create(
                usuario=user,
                telefone=form.cleaned_data.get('telefone')
            )

            # 5. Loga e Redireciona
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.first_name}!")
            return redirect('listar_tarefas') 
    else:
        form = CadastroForm()
    
    return render(request, 'usuarios/cadastro.html', {'form': form})
# --- VIEWS PROTEGIDAS (PRECISAM DE LOGIN) ---

@login_required
def listar_tarefas(request):
    # Filtro essencial: apenas minhas tarefas e que não estão na "lixeira"
    tarefas = Tarefa.objects.filter(usuario=request.user, excluida=False).order_by('-criado_em')
    
    context = {
        'tarefas': tarefas,
        'total': tarefas.count(),
        'pendentes': tarefas.filter(finalizado=False).count(),
        'finalizadas': tarefas.filter(finalizado=True).count(),
    }
    return render(request, 'tarefas/listar.html', context)

@login_required
def nova_tarefa(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if titulo:
            Tarefa.objects.create(
                usuario=request.user, # Define o dono da tarefa
                titulo=titulo, 
                descricao=descricao
            )
            return redirect('listar_tarefas')

    return render(request, 'tarefas/nova.html')

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)

    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.descricao = request.POST.get('descricao')
        tarefa.finalizado = 'finalizado' in request.POST
        tarefa.save()
        return redirect('listar_tarefas')

    return render(request, 'tarefas/editar.html', {'tarefa': tarefa})

@login_required
def detalhes_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    return render(request, 'tarefas/detalhe.html', {'tarefa': tarefa})

@login_required
def deletar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)

    if request.method == 'POST':
        tarefa.excluida = True  # Soft delete aplicado
        tarefa.save()

    return redirect('listar_tarefas')