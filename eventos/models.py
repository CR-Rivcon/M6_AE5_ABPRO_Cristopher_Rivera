from django.db import models
from django.contrib.auth.models import User


class Evento(models.Model):
	nombre = models.CharField(max_length=100)
	fecha = models.DateField()
	ubicacion = models.CharField(max_length=255, blank=True)
	es_privado = models.BooleanField(default=False)
	organizador = models.ForeignKey(User, related_name="eventos_organizados", on_delete=models.CASCADE, null=True, blank=True)
	creado_en = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"{self.nombre} ({self.fecha})"


class Participante(models.Model):
	evento = models.ForeignKey(Evento, related_name="participantes", on_delete=models.CASCADE)
	nombre = models.CharField(max_length=120)
	email = models.EmailField()
	usuario = models.ForeignKey(User, related_name="participaciones", on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self) -> str:
		return f"{self.nombre} - {self.email}"
