from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from Tarefas.models import *

def Cadastro_Tarefa(request):
    print(request.method)
    if request.method == "POST":
        form = TarefaForm(request.POST)
        formset = AnexoFormSet(request.POST, request.FILES, queryset=Tasks_Attachments.objects.none())

        print("form.is_valid():", form.is_valid())
        print("formset.is_valid():", formset.is_valid())
        print("Form errors:", form.errors)


        if form.is_valid(): 
            # Salva a tarefa
            tarefa = form.save(commit=False)
                        
            if not tarefa.STATUS_id:
                tarefa.STATUS = Tasks_Status.objects.first()
            tarefa.save()

        if formset.is_valid():
            for anexo in formset.save(commit=False):
                anexo.TASK = tarefa
                anexo.save()                

        return redirect("Listar")
    else:
        form = TarefaForm()
        formset = AnexoFormSet(queryset=Tasks_Attachments.objects.none())

    return render(
        request,
        "Tarefas/Cadastro_Tarefa.html",
        {"form": form, "formset": formset}
    )

def Listar_Tarefas(request):
    status_list = Tasks_Status.objects.all()
    status_filter = request.GET.get("status")

    tarefas = Tasks.objects.select_related('STATUS', 'PRIORIDADE').order_by('DESCRICAO')
    if status_filter and status_filter != "todos":
        tarefas = tarefas.filter(STATUS_id=status_filter)

    return render(request, "Tarefas/Lista_Tarefa.html", {
        "tarefas": tarefas,
        "status_list": status_list,
        "status_filter": status_filter
    })

def Ver_Tarefa(request, Id):
    tarefa = get_object_or_404(
        Tasks.objects.select_related("STATUS", "PRIORIDADE"),
        id=Id
    )
    imagens = tarefa.anexos.filter(TIPO__DESCRICAO__iexact="IMAGEM")
    pdfs = tarefa.anexos.filter(TIPO__DESCRICAO__iexact="PDF")
    comentarios = tarefa.comments.order_by('-REGISTRADO')

    form_anexos = AnexoFormSet(queryset=Tasks_Attachments.objects.none())

    if request.method == "POST":

        if "editar_descricao" in request.POST:
            nova_descricao = request.POST.get("DESCRICAO")
            if nova_descricao:
                tarefa.DESCRICAO = nova_descricao
                tarefa.save()
            return redirect('Tarefa', Id=tarefa.id)

        if "salvar_status_prioridade" in request.POST:
            nova_status_id = request.POST.get("STATUS")
            nova_prioridade_id = request.POST.get("PRIORIDADE")
            if nova_status_id:
                tarefa.STATUS_id = int(nova_status_id)
            if nova_prioridade_id:
                tarefa.PRIORIDADE_id = int(nova_prioridade_id)
            tarefa.save()
            return redirect('Tarefa', Id=tarefa.id)

        else:
            form_comentario = ComentarioForm(request.POST)
            if form_comentario.is_valid():
                novo = form_comentario.save(commit=False)
                novo.TASK = tarefa
                novo.save()
                return redirect('Tarefa', Id=tarefa.id)
    else:
        form_comentario = ComentarioForm()

    status_list = Tasks_Status.objects.all()
    prioridade_list = Tasks_Prioridade.objects.all()

    return render(request, "Tarefas/Tarefa.html", {
        "tarefa": tarefa,
        "imagens": imagens,
        "pdfs": pdfs,
        "comentarios": comentarios,
        "form_comentario": form_comentario,
        "status_list": status_list,
        "prioridade_list": prioridade_list,
        "form_anexos": form_anexos
    })

def Excluir_Comentario(request, comentario_id):
    comentario = get_object_or_404(Tasks_Comments, id=comentario_id)
    tarefa_id = comentario.TASK.id
    if request.method == "POST":
        comentario.delete()
    return redirect('Tarefa', Id=tarefa_id)

def Salvar_Anexo_Novo(request,Id):

    if request.method == "POST":

        tarefa = get_object_or_404(
            Tasks.objects.select_related("STATUS", "PRIORIDADE"),
            id=Id
        )

        formset = AnexoFormSet(
                request.POST or None,
                request.FILES or None,
                queryset=tarefa.anexos.all()
        )

        if formset.is_valid():
            for anexo in formset.save(commit=False):
                anexo.TASK = tarefa
                anexo.save()

    return redirect('Tarefa', Id=tarefa.id)    

def excluir_anexo(request, anexo_id):
    anexo = get_object_or_404(Tasks_Attachments, id=anexo_id)
    tarefa_id = anexo.TASK.id  # Guardar id da tarefa para redirecionar
    anexo.delete()
    return redirect('Tarefa', Id=tarefa_id)