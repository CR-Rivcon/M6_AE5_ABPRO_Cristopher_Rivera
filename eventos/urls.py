from django.urls import path

from .views import registrar_evento

urlpatterns = [
	path("", registrar_evento, name="registrar_evento"),
]


