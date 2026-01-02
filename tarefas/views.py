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
            user = form.save(commit=False)
            
            # Pega o email e define como username (garante login via email)
            email_digitado = form.cleaned_data.get('email')
            user.username = email_digitado 
            
            # Define a senha de forma criptografada (ESSENCIAL)
            user.set_password(form.cleaned_data.get('senha'))
            
            # Pega o nome completo e separa em first_name para o avatar
            nome_completo = form.cleaned_data.get('nome')
            if nome_completo:
                partes = nome_completo.split(' ', 1)
                user.first_name = partes[0]
                user.last_name = partes[1] if len(partes) > 1 else ""

            user.save()

            # Cria o perfil vinculado (Telefone)
            Perfil.objects.create(
                usuario=user,
                telefone=form.cleaned_data.get('telefone')
            )

            login(request, user)
            messages.success(request, f"🚀 Bem-vindo, {user.first_name}! Sua conta foi criada.")
            return redirect('listar_tarefas') 
    else:
        form = CadastroForm()
    
    return render(request, 'usuarios/cadastro.html', {'form': form})

# --- VIEWS PROTEGIDAS ---

@login_required
def listar_tarefas(request):
    # 1. Base: Tarefas do usuário que não estão na lixeira
    queryset_base = Tarefa.objects.filter(usuario=request.user, excluida=False)
    
    # 2. Captura o filtro da URL (os botões que criamos no HTML)
    status_filtro = request.GET.get('status', 'todas')
    
    if status_filtro == 'pendentes':
        tarefas = queryset_base.filter(finalizado=False)
    elif status_filtro == 'concluidas':
        tarefas = queryset_base.filter(finalizado=True)
    else:
        tarefas = queryset_base

    # 3. Contexto com contadores reais
    context = {
        'tarefas': tarefas.order_by('-criado_em'),
        'total': queryset_base.count(),
        'pendentes': queryset_base.filter(finalizado=False).count(),
        'finalizadas': queryset_base.filter(finalizado=True).count(),
    }
    return render(request, 'tarefas/listar.html', context)

@login_required
def nova_tarefa(request):
    """View que processa o formulário que está dentro do Drawer lateral"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if titulo:
            Tarefa.objects.create(
                usuario=request.user,
                titulo=titulo, 
                descricao=descricao
            )
            messages.success(request, "Tarefa criada com sucesso!")
            return redirect('listar_tarefas')
        else:
            messages.error(request, "O título da tarefa é obrigatório.")

    # Se alguém acessar via GET, mandamos de volta para a lista (onde o drawer vive)
    return redirect('listar_tarefas')

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)

    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.descricao = request.POST.get('descricao')
        # Checkbox: se vier na request, é True
        tarefa.finalizado = 'finalizado' in request.POST
        tarefa.save()
        messages.success(request, "Tarefa atualizada!")
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
        tarefa.excluida = True  # Soft delete
        tarefa.save()
        messages.warning(request, "Tarefa enviada para a lixeira.")

    return redirect('listar_tarefas')