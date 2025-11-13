from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import EventoForm, ParticipanteFormSet
from .models import Evento


class AccesoDenegadoView(View):
	def get(self, request):
		return render(request, "eventos/acceso_denegado.html", status=403)


class EventoListaView(LoginRequiredMixin, ListView):
	model = Evento
	template_name = "eventos/evento_lista.html"
	context_object_name = "eventos"

	def get_queryset(self):
		user = self.request.user
		if user.is_superuser or user.groups.filter(name="Administradores").exists():
			return Evento.objects.all().order_by("-fecha", "-creado_en")
		if user.groups.filter(name="Organizadores").exists():
			return Evento.objects.filter(organizador=user).order_by("-fecha", "-creado_en")
		# Asistentes: sólo eventos a los que están inscritos
		return Evento.objects.filter(participantes__usuario=user).distinct().order_by("-fecha", "-creado_en")


class EventoDetalleView(LoginRequiredMixin, DetailView):
	model = Evento
	template_name = "eventos/evento_detalle.html"
	context_object_name = "evento"

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		user = request.user
		if not obj.es_privado:
			return super().dispatch(request, *args, **kwargs)
		# privado: permitir al admin, organizador o asistentes inscritos
		if user.is_superuser or obj.organizador_id == user.id or obj.participantes.filter(usuario=user).exists():
			return super().dispatch(request, *args, **kwargs)
		messages.error(request, "No tienes permisos para ver este evento privado.")
		return render(request, "eventos/acceso_denegado.html", status=403)


class EventoCrearView(LoginRequiredMixin, PermissionRequiredMixin, View):
	permission_required = "eventos.add_evento"
	raise_exception = False

	def handle_no_permission(self):
		if self.request.user.is_authenticated:
			messages.error(self.request, "No tienes permiso para crear eventos.")
			return redirect("acceso_denegado")
		return super().handle_no_permission()

	def get(self, request):
		evento_form = EventoForm()
		formset = ParticipanteFormSet()
		return render(request, "eventos/evento_form.html", {"evento_form": evento_form, "formset": formset})

	def post(self, request):
		evento_form = EventoForm(request.POST)
		formset = ParticipanteFormSet(request.POST)
		if evento_form.is_valid() and formset.is_valid():
			evento = evento_form.save(commit=False)
			evento.organizador = request.user
			evento.save()
			formset.instance = evento
			formset.save()
			messages.success(request, "Evento creado correctamente.")
			return redirect("eventos_lista")
		return render(request, "eventos/evento_form.html", {"evento_form": evento_form, "formset": formset})


class EventoEditarView(LoginRequiredMixin, PermissionRequiredMixin, View):
	permission_required = "eventos.change_evento"
	raise_exception = False

	def handle_no_permission(self):
		if self.request.user.is_authenticated:
			messages.error(self.request, "No tienes permiso para editar eventos.")
			return redirect("acceso_denegado")
		return super().handle_no_permission()

	def get_obj(self, pk):
		return Evento.objects.get(pk=pk)

	def get(self, request, pk):
		evento = self.get_obj(pk)
		# organizadores solo pueden editar los suyos
		if request.user.groups.filter(name="Organizadores").exists() and evento.organizador_id != request.user.id and not request.user.is_superuser:
			raise PermissionDenied
		evento_form = EventoForm(instance=evento)
		formset = ParticipanteFormSet(instance=evento)
		return render(request, "eventos/evento_form.html", {"evento_form": evento_form, "formset": formset})

	def post(self, request, pk):
		evento = self.get_obj(pk)
		if request.user.groups.filter(name="Organizadores").exists() and evento.organizador_id != request.user.id and not request.user.is_superuser:
			raise PermissionDenied
		evento_form = EventoForm(request.POST, instance=evento)
		formset = ParticipanteFormSet(request.POST, instance=evento)
		if evento_form.is_valid() and formset.is_valid():
			evento_form.save()
			formset.save()
			messages.success(request, "Evento actualizado correctamente.")
			return redirect("eventos_detalle", pk=evento.pk)
		return render(request, "eventos/evento_form.html", {"evento_form": evento_form, "formset": formset})
