# KIWI v4 — Asistente Pedagógico con IA para Docentes

Aplicación web para docentes de educación socioemocional del **Colegio San Francisco de Asís (Cali, Colombia)**. Permite gestionar clases, generar actividades pedagógicas con IA y sincronizar con Google Calendar.

---

## Instalación rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env y pegar la API key de Gemini (aistudio.google.com)

# 3. Crear base de datos
python manage.py migrate

# 4. Iniciar servidor
python manage.py runserver

# 5. Abrir en el navegador
http://127.0.0.1:8000
```

---

## Variables de entorno requeridas (.env)

```bash
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
GEMINI_API_KEY=tu-api-key-de-gemini     # Obligatorio para Kleit IA
GEMINI_MODEL=gemini-2.0-flash
GOOGLE_CLIENT_ID=...                     # Opcional — Google Calendar
GOOGLE_CLIENT_SECRET=...                 # Opcional — Google Calendar
```

---

## Funcionalidades principales

### Kleit — Motor de IA Pedagógico
Genera 3 actividades de educación socioemocional personalizadas a partir de un tema y grupo. Usa **Google Gemini 2.0-Flash** como motor principal, con fallback automático a un banco de 30+ actividades verificadas con fuentes científicas (APA, CASEL, Yale, Seligman, MEN Colombia).

- Verifica el estado en: `http://127.0.0.1:8000/api/kleit/estado/`

### Calendario de Clases
- Crear clases únicas o recurrentes (semanal / quincenal)
- Marcar clases como completadas y registrar satisfacción (1–10)
- Sincronización bidireccional con Google Calendar (OAuth2)

### Plan de Aula con IA
Genera planes de aula completos por grado (jardín → 11°), período y competencia SEL. Incluye desempeño, temas, estrategia pedagógica, valoración continua y rúbricas.

### Recursos y Tareas
- Biblioteca de recursos clasificados por ciclo educativo y tipo
- Gestión de tareas personales con estados (no empezada / en proceso / completada)

---

## Arquitectura

| Componente | Tecnología |
|-----------|-----------|
| Backend | Django 4.2–6.0, Python 3.x |
| Base de datos | SQLite3 (desarrollo) |
| IA generativa | Google Gemini 2.0-Flash |
| Frontend | Bootstrap 5.3.2 + Vanilla JS |
| Calendario externo | Google Calendar API (OAuth2) |

**Archivos clave:**
- `kiwi/kleit_engine.py` — Motor de IA: prompt, few-shot examples, banco local, conexión a Gemini
- `kiwi/psicologia_db.py` — Banco de actividades psicológicamente verificadas
- `kiwi/views.py` — Lógica de toda la aplicación
- `kiwi/google_calendar.py` — Integración OAuth2 con Google Calendar

---

## Rutas principales

```
/              → Landing page
/login/        → Inicio de sesión
/registro/     → Registro de nuevo docente
/dashboard/    → Panel principal
/calendario/   → Gestión de clases
/kleit/        → Generador de actividades con IA
/plan-aula/    → Planes de aula
/recursos/     → Biblioteca de recursos
/tareas/       → Gestor de tareas
```

---

## Para desarrolladores

Ver [CLAUDE.md](CLAUDE.md) para guía de arquitectura, convenciones y problemas conocidos.
