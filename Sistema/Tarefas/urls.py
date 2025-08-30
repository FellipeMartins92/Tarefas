from django.urls import path
from . import views

urlpatterns = [
    path('Cadastro/', views.Cadastro_Tarefa,name='Cadastro'),
    path('Listar/', views.Listar_Tarefas,name='Listar'),
    path('Comentario/Excluir/<int:comentario_id>/', views.Excluir_Comentario, name='excluir_comentario'),
    path('Tarefa/Salvar_Anexo_Novo/<int:Id>/', views.Salvar_Anexo_Novo, name='Salvar_Anexo_Novo'),
    path('anexo/excluir/<int:anexo_id>/', views.excluir_anexo, name='excluir_anexo'),
    path('Tarefa/<int:Id>/', views.Ver_Tarefa,name='Tarefa'),
]