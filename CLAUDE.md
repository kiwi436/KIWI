# CLAUDE.md — Guía de desarrollo KIWI v4

## Qué es este proyecto

**K.I.W.I. v4** es una aplicación web Django monolítica (MVT) para docentes de educación socioemocional del Colegio San Francisco de Asís (Cali, Colombia). Permite gestionar clases, generar actividades pedagógicas con IA (Gemini) y sincronizar con Google Calendar.

## Comandos esenciales

```bash
# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones (siempre después de cambiar models.py)
python manage.py migrate

# Crear migración nueva
python manage.py makemigrations

# Servidor de desarrollo
python manage.py runserver

# Shell Django (para inspeccionar BD)
python manage.py shell

# Panel de administración: http://127.0.0.1:8000/admin/
python manage.py createsuperuser
```

## Arquitectura del proyecto

```
config/
  settings.py       → Zona: America/Bogota, idioma: es-co, BD: SQLite, sesiones en BD
  urls.py           → Incluye kiwi.urls

kiwi/
  models.py         → 7 modelos: Usuario, Clase, Tarea, Recurso, IdeaKleit, SesionKleit, PlanDeAula
  views.py          → 47 vistas (~857 líneas), lógica de toda la app
  urls.py           → 50+ rutas
  kleit_engine.py   → Motor IA: Gemini + banco local de fallback ⭐
  psicologia_db.py  → Banco de 30+ actividades verificadas (fuentes APA, CASEL, Yale, etc.)
  google_calendar.py→ OAuth2 con Google Calendar (sin SDK externo, usa urllib)
  admin.py          → Modelos registrados en el panel de admin
  templates/kiwi/   → 12 archivos HTML con Bootstrap 5 + CSS custom
```

## Archivos críticos y su propósito

| Archivo | Rol |
|---------|-----|
| `kiwi/kleit_engine.py` | SYSTEM_PROMPT, few-shot examples, banco local, llamada a Gemini. Tocar con cuidado. |
| `kiwi/psicologia_db.py` | Banco psicológico de fallback. Agregar actividades aquí si se amplía. |
| `kiwi/models.py` | Cualquier cambio requiere `makemigrations` + `migrate`. |
| `kiwi/views.py` | Función `_login_required(request)` protege todas las rutas autenticadas. |
| `kiwi/google_calendar.py` | OAuth2 manual. Tokens guardados en `request.session`. |
| `config/settings.py` | `SESSION_COOKIE_AGE = 86400` (1 día), sesiones en BD. |

## Variables de entorno (.env)

```bash
DJANGO_SECRET_KEY=...          # Cambiar en producción
DEBUG=True                     # Cambiar a False en producción
GEMINI_API_KEY=...             # Obligatorio para Kleit real (aistudio.google.com)
GEMINI_MODEL=gemini-2.0-flash  # Modelo de Gemini a usar
GOOGLE_CLIENT_ID=...           # Opcional — solo si se usa Google Calendar
GOOGLE_CLIENT_SECRET=...       # Opcional — solo si se usa Google Calendar
```

## Modelos de datos

**Importante:** Los modelos `Clase`, `Tarea`, `Recurso`, `IdeaKleit`, `SesionKleit` y `PlanDeAula` **no tienen FK al modelo `Usuario`** — los datos son globales, no están separados por usuario. Tener esto en cuenta al agregar features o filtros.

### Relaciones clave
- `Clase` tiene FK a sí misma (`clase_padre`) para manejar recurrencia semanal/quincenal
- `IdeaKleit` tiene FK opcional a `Clase` (cuando se asigna a una clase)
- `SesionKleit` tiene M2M a `IdeaKleit`

## Autenticación

- Sesiones Django en BD (no JWT, no Django auth)
- La sesión guarda: `usuario_nombre`, `usuario_correo`, `usuario_institucion`
- Guard: `_login_required(request)` en `views.py` — redirige a `/login/` si falla
- Las contraseñas se guardan en `password_hash` con lógica propia (no Django's `make_password`)

## El Motor Kleit (kleit_engine.py)

Flujo de `generar_ideas(tema, grupo, historial_titulos)`:
1. `detectar_nivel(grupo)` → primaria / bachillerato / general
2. `detectar_categoria(tema)` → 8 categorías emocionales
3. `_intentar_con_gemini()` → llama Gemini con SYSTEM_PROMPT + few-shot examples → JSON con 3 ideas
4. Si falla → `_banco_local_fallback()` → selecciona del banco psicológico local

Para plan de aula: `_generar_plan_con_ia()` en `views.py` con timeout de 110s, fallback a `_plan_local()`.

## Frontend

- **Bootstrap 5.3.2** (CDN) + CSS custom en `<style>` dentro de `base.html`
- **Modo oscuro:** `data-theme="dark"` en `<html>`, variables CSS cambian automáticamente
- **Vanilla JS + Fetch API** para llamadas AJAX (no hay framework JS)
- Las APIs JSON están en `/api/*` y retornan `JsonResponse`
- Iconos: Font Awesome 6.5 (CDN)

## Endpoints de la API JSON

```
GET /api/clases/           → Clases en formato FullCalendar
GET /api/notificaciones/   → Clases en próximos 15 minutos
GET /api/kleit/estado/     → Estado de Gemini (activo/fallback/sin_key)
GET /api/google/eventos/   → Eventos del Google Calendar conectado
GET /api/frase-dia/        → Frase motivacional del día
```

## Rutas del panel de administración Django

```
/admin/   → Panel admin (requiere superuser creado con manage.py createsuperuser)
```

## Configuración de Google Calendar

El flujo OAuth2 está en `google_calendar.py` y las vistas en `views.py`:
- `/calendario/google/conectar/` → inicia el flujo OAuth
- `/calendario/google/callback/` → recibe el code y obtiene tokens
- Tokens se guardan en `request.session` (no en BD)
- Refresh automático cuando el token expira

## Problemas conocidos / Deuda técnica

1. **Multi-usuario roto:** Los modelos no tienen FK a Usuario. Si hay dos docentes, comparten todos los datos.
2. **Contraseñas:** `password_hash` no usa `django.contrib.auth.hashers` — revisar antes de producción.
3. **Producción:** Cambiar `DEBUG=False`, `ALLOWED_HOSTS` específico y migrar de SQLite a PostgreSQL.
4. **Tokens Google:** Se guardan en sesión, no en BD — se pierden al expirar la sesión.

## Convenciones del proyecto

- Idioma del código: español (nombres de variables, comentarios, mensajes)
- Zona horaria: `America/Bogota`
- Formato de fechas: Django localización `es-co`
- Los templates usan `{% load ... %}` con tags personalizados en `kiwi/templatetags/`
