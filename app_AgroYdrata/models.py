from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Dados(models.Model):
    id_dados = models.AutoField(primary_key=True)
    nitrogenio = models.DecimalField(max_digits=5, decimal_places=2)
    fosforo = models.DecimalField(max_digits=5, decimal_places=2)
    potassio = models.DecimalField(max_digits=5, decimal_places=2)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    umidade = models.DecimalField(max_digits=5, decimal_places=2)
    ph = models.DecimalField(max_digits=5, decimal_places=2)
    precipitacao = models.DecimalField(max_digits=5, decimal_places=2)
    tp_planta = models.TextField(max_length=100)
    resultado = models.FloatField(default=0.0)
    data_insercao = models.DateField(default=timezone.now)
    horario_insercao = models.TimeField(default=timezone.now)
    
    usuario = models.ForeignKey(
        to=CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="user",
    )
