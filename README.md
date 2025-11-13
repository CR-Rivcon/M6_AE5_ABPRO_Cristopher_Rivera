# Registro de Eventos (Django + Bootstrap)

Proyecto básico de estudiante para registrar eventos y participantes usando Django, formularios y plantillas reutilizables con Bootstrap. Base de datos: SQLite.

## Requisitos
- Python 3.10+ (recomendado)
- Pip

## Instalación (Windows PowerShell)
```powershell
cd "C:\Users\Cris-pc\Desktop\M6_AE4_ABPRO_Cristopher_Rivera"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Migraciones y superusuario
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Ejecutar el servidor
```powershell
python manage.py runserver
```
Abrir `http://127.0.0.1:8000/` para ver el formulario de registro de eventos.

Panel de administración: `http://127.0.0.1:8000/admin/`

## Estructura funcional
- Modelos:
  - `Evento`: nombre (máx. 100), fecha futura obligatoria, ubicación opcional
  - `Participante`: nombre y email, relacionado a un evento
- Formularios:
  - `EventoForm` con validación de fecha futura
  - `ParticipanteForm` y `ParticipanteFormSet` para múltiples participantes
- Vistas:
  - `registrar_evento`: GET (muestra formularios), POST (valida y guarda)
- Templates:
  - `base.html` con Bootstrap
  - `evento_form.html` + parciales `_evento_fields.html` y `_participante_form.html`

## Notas
- Se usa SQLite por defecto (archivo `db.sqlite3`).
- Para cambiar el idioma a español ya está configurado en `settings.py`.


