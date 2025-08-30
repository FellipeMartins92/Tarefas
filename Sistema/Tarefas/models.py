from django.db import models
from django.utils.timezone import now


class Tasks_Prioridade(models.Model):
    DESCRICAO = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.DESCRICAO}"

class Tasks_Status(models.Model):
    DESCRICAO = models.TextField(max_length=100)    

    def __str__(self):
        return f"{self.DESCRICAO}"

class Tasks(models.Model):
    DESCRICAO = models.TextField(max_length=100)
    REGISTRADO = models.DateTimeField(default=now)
    PRIORIDADE = models.ForeignKey(Tasks_Prioridade, on_delete=models.CASCADE, related_name="PRIORIDADE")
    STATUS = models.ForeignKey(Tasks_Status, on_delete=models.CASCADE, related_name="STATUS")

class Tipo_Attachments(models.Model):
    DESCRICAO = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.DESCRICAO}"

class Tasks_Attachments(models.Model):
    TASK = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        related_name="anexos"
    )
    TIPO = models.ForeignKey(
        Tipo_Attachments,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="anexos"
    )
    ANEXO = models.FileField(upload_to="anexos/")

    def __str__(self):
        return f"{self.TIPO} - {self.ANEXO.name if self.ANEXO else 'sem arquivo'}"

class Tasks_Comments(models.Model):
    TASK = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name="comments")    
    COMENTARIO = models.TextField(max_length=1000)
    REGISTRADO = models.DateTimeField(default=now)