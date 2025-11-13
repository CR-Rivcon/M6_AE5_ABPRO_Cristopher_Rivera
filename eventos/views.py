from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import EventoForm, ParticipanteFormSet


def registrar_evento(request):
	if request.method == "POST":
		evento_form = EventoForm(request.POST)
		formset = ParticipanteFormSet(request.POST)
		if evento_form.is_valid() and formset.is_valid():
			evento = evento_form.save()
			formset.instance = evento
			formset.save()
			messages.success(request, "Evento registrado correctamente.")
			return redirect("registrar_evento")
	else:
		evento_form = EventoForm()
		formset = ParticipanteFormSet()

	context = {
		"evento_form": evento_form,
		"formset": formset,
	}
	return render(request, "eventos/evento_form.html", context)
