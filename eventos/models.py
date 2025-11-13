from django.db import models


class Evento(models.Model):
	nombre = models.CharField(max_length=100)
	fecha = models.DateField()
	ubicacion = models.CharField(max_length=255, blank=True)
	creado_en = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"{self.nombre} ({self.fecha})"


class Participante(models.Model):
	evento = models.ForeignKey(Evento, related_name="participantes", on_delete=models.CASCADE)
	nombre = models.CharField(max_length=120)
	email = models.EmailField()

	def __str__(self) -> str:
		return f"{self.nombre} - {self.email}"
