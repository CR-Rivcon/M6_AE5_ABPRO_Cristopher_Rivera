from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from .models import Evento, Participante


class EventoForm(forms.ModelForm):
	class Meta:
		model = Evento
		fields = ["nombre", "fecha", "ubicacion", "es_privado"]
		widgets = {
			"fecha": forms.DateInput(attrs={"type": "date"}),
		}

	def clean_fecha(self):
		fecha = self.cleaned_data.get("fecha")
		if fecha and fecha <= timezone.localdate():
			raise forms.ValidationError("La fecha del evento debe ser futura.")
		return fecha


class ParticipanteForm(forms.ModelForm):
	class Meta:
		model = Participante
		fields = ["nombre", "email", "usuario"]


ParticipanteFormSet = inlineformset_factory(
	Evento,
	Participante,
	form=ParticipanteForm,
	extra=1,
	min_num=1,
	validate_min=True,
	can_delete=False,
)


