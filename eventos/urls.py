from django.urls import path

from .views import (
	AccesoDenegadoView,
	EventoCrearView,
	EventoDetalleView,
	EventoEditarView,
	EventoListaView,
)

urlpatterns = [
	path("", EventoListaView.as_view(), name="eventos_lista"),
	path("eventos/nuevo/", EventoCrearView.as_view(), name="eventos_crear"),
	path("eventos/<int:pk>/", EventoDetalleView.as_view(), name="eventos_detalle"),
	path("eventos/<int:pk>/editar/", EventoEditarView.as_view(), name="eventos_editar"),
	path("acceso-denegado/", AccesoDenegadoView.as_view(), name="acceso_denegado"),
]


