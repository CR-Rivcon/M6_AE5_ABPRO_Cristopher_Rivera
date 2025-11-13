from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from eventos.models import Evento


class Command(BaseCommand):
	help = "Crea grupos y asigna permisos para Administradores, Organizadores y Asistentes"

	def handle(self, *args, **options):
		# Obtener permisos del modelo Evento
		ct_evento = ContentType.objects.get_for_model(Evento)
		add_evento = Permission.objects.get(codename="add_evento", content_type=ct_evento)
		change_evento = Permission.objects.get(codename="change_evento", content_type=ct_evento)
		delete_evento = Permission.objects.get(codename="delete_evento", content_type=ct_evento)

		# Administradores: todos los permisos de evento
		admins, _ = Group.objects.get_or_create(name="Administradores")
		admins.permissions.set([add_evento, change_evento, delete_evento])

		# Organizadores: crear y editar, pero no borrar
		orgs, _ = Group.objects.get_or_create(name="Organizadores")
		orgs.permissions.set([add_evento, change_evento])

		# Asistentes: sin permisos especiales de edición/creación
		asist, _ = Group.objects.get_or_create(name="Asistentes")
		asist.permissions.clear()

		self.stdout.write(self.style.SUCCESS("Grupos y permisos configurados."))


