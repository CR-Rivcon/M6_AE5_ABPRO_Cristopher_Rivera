from django.contrib import admin

from .models import Evento, Participante


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
	list_display = ("nombre", "fecha", "ubicacion", "creado_en")
	search_fields = ("nombre", "ubicacion")
	list_filter = ("fecha",)


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
	list_display = ("nombre", "email", "evento")
	search_fields = ("nombre", "email", "evento__nombre")
