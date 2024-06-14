from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Archivo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='archivos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_archivo

class Grafica(models.Model):
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)
    tipo_grafica = models.CharField(max_length=100)
    parametros = models.JSONField()
    imagen_grafica = models.ImageField(upload_to='images/')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.tipo_grafica