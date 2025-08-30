from django import forms
from django.forms import modelformset_factory
from .models import *

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["DESCRICAO", "PRIORIDADE", "STATUS"]
        widgets = {
            "DESCRICAO": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Digite a descrição da tarefa"
            }),
            "PRIORIDADE": forms.Select(attrs={"class": "form-select"}),
            "STATUS": forms.Select(attrs={"class": "form-select"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['STATUS'].empty_label = None
        self.fields['PRIORIDADE'].empty_label = None
        

class AnexoForm(forms.ModelForm):
    class Meta:
        model = Tasks_Attachments
        fields = ["TIPO", "ANEXO"]
        widgets = {
            "TIPO": forms.Select(attrs={"class": "form-select"}),
            "ANEXO": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['TIPO'].empty_label = None

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Tasks_Comments
        fields = ['COMENTARIO']
        widgets = {
            'COMENTARIO': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Escreva seu comentário...'})
        }


AnexoFormSet = modelformset_factory(
    Tasks_Attachments,
    form=AnexoForm,
    extra=1,
    can_delete=True
)




