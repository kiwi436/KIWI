"""
╔══════════════════════════════════════════════════════════════╗
║     INTEGRACIÓN GOOGLE CALENDAR — K.I.W.I. v4              ║
║     Flujo OAuth2 completo sin librerías de Google           ║
╚══════════════════════════════════════════════════════════════╝

CÓMO OBTENER TUS CREDENCIALES (pasos rápidos):
1. Ve a https://console.cloud.google.com
2. Crea un proyecto nuevo → "KIWI Calendario"
3. APIs & Services → Enable APIs → busca "Google Calendar API" → Enable
4. Credentials → Create Credentials → OAuth 2.0 Client ID
5. Application type: Web application
6. Authorized redirect URIs: http://localhost:8000/calendario/google/callback/
7. Descarga el JSON → copia client_id y client_secret en tu .env

VARIABLES EN .env:
  GOOGLE_CLIENT_ID=tu_client_id.apps.googleusercontent.com
  GOOGLE_CLIENT_SECRET=tu_client_secret
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import logging
from datetime import datetime, timezone as tz

from django.conf import settings

logger = logging.getLogger(__name__)

# ── OAuth2 endpoints ────────────────────────────────────────────
GOOGLE_AUTH_URL   = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL  = "https://oauth2.googleapis.com/token"
GOOGLE_REVOKE_URL = "https://oauth2.googleapis.com/revoke"
CALENDAR_BASE     = "https://www.googleapis.com/calendar/v3"

SCOPES = "https://www.googleapis.com/auth/calendar"


# ══════════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ══════════════════════════════════════════════════════════════════

def get_auth_url(request) -> str:
    """Genera la URL de autorización de Google para redirigir al usuario."""
    client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    if not client_id:
        raise ValueError("GOOGLE_CLIENT_ID no configurado en .env")

    redirect_uri = _get_redirect_uri(request)
    params = {
        "client_id":     client_id,
        "redirect_uri":  redirect_uri,
        "response_type": "code",
        "scope":         SCOPES,
        "access_type":   "offline",
        "prompt":        "consent",
        "state":         "kiwi_calendar_auth",
    }
    return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"


def exchange_code_for_tokens(request, code: str) -> dict:
    """Intercambia el código de autorización por access_token + refresh_token."""
    client_id     = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', '')
    redirect_uri  = _get_redirect_uri(request)

    data = urllib.parse.urlencode({
        "code":          code,
        "client_id":     client_id,
        "client_secret": client_secret,
        "redirect_uri":  redirect_uri,
        "grant_type":    "authorization_code",
    }).encode()

    try:
        req  = urllib.request.Request(GOOGLE_TOKEN_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            tokens = json.loads(resp.read())
        return tokens
    except Exception as e:
        logger.error(f"Google token exchange error: {e}")
        return {}


def refresh_access_token(refresh_token: str) -> str | None:
    """Refresca el access_token usando el refresh_token guardado."""
    client_id     = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', '')

    data = urllib.parse.urlencode({
        "refresh_token": refresh_token,
        "client_id":     client_id,
        "client_secret": client_secret,
        "grant_type":    "refresh_token",
    }).encode()

    try:
        req = urllib.request.Request(GOOGLE_TOKEN_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
        return result.get("access_token")
    except Exception as e:
        logger.error(f"Google token refresh error: {e}")
        return None


def _get_redirect_uri(request) -> str:
    site_url = getattr(settings, 'SITE_URL', '').rstrip('/')
    if site_url:
        return f"{site_url}/google/callback/"
    scheme = "https" if request.is_secure() else "http"
    return f"{scheme}://{request.get_host()}/google/callback/"


def _get_valid_token(session) -> str | None:
    """Retorna un access_token válido, refrescándolo si es necesario."""
    access_token  = session.get('google_access_token')
    refresh_token = session.get('google_refresh_token')
    expires_at    = session.get('google_token_expires', 0)

    import time
    if access_token and time.time() < expires_at - 60:
        return access_token

    if refresh_token:
        new_token = refresh_access_token(refresh_token)
        if new_token:
            session['google_access_token']    = new_token
            session['google_token_expires']   = int(time.time()) + 3600
            session.modified = True
            return new_token

    return None


def is_connected(session) -> bool:
    """Retorna True si el usuario tiene Google Calendar conectado."""
    return bool(session.get('google_refresh_token'))


# ══════════════════════════════════════════════════════════════════
# OPERACIONES DE CALENDARIO
# ══════════════════════════════════════════════════════════════════

def _api_request(session, method: str, endpoint: str, body: dict = None) -> dict | None:
    """Hace una petición autenticada a la Google Calendar API."""
    token = _get_valid_token(session)
    if not token:
        return None

    url = f"{CALENDAR_BASE}{endpoint}"
    data = json.dumps(body).encode() if body else None

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_err = e.read().decode()
        logger.error(f"Google Calendar API {method} {endpoint} → {e.code}: {body_err}")
        return None
    except Exception as e:
        logger.error(f"Google Calendar API error: {e}")
        return None


def crear_evento_google(session, clase) -> str | None:
    """
    Crea un evento en Google Calendar a partir de una Clase de KIWI.
    Retorna el google_event_id si tuvo éxito, None si falló.
    """
    from django.utils import timezone

    # Construir fechas en formato RFC3339
    inicio  = clase.fecha
    fin     = clase.fecha + __import__('datetime').timedelta(minutes=60)

    body = {
        "summary":     f"🏫 {clase.titulo} — {clase.grupo}",
        "description": (
            f"Clase de gestión emocional\n"
            f"Grupo: {clase.grupo}\n"
            f"Tema: {clase.tema or 'Sin especificar'}\n"
            f"Notas: {clase.notas or ''}\n\n"
            f"📱 Creado desde K.I.W.I."
        ),
        "start": {
            "dateTime": inicio.isoformat(),
            "timeZone": "America/Bogota",
        },
        "end": {
            "dateTime": fin.isoformat(),
            "timeZone": "America/Bogota",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup",  "minutes": 15},
                {"method": "email",  "minutes": 60},
            ],
        },
        "colorId": "9",  # Azul en Google Calendar
    }

    result = _api_request(session, "POST", "/calendars/primary/events", body)
    if result:
        event_id = result.get("id")
        logger.info(f"Evento creado en Google Calendar: {event_id}")
        return event_id
    return None


def actualizar_evento_google(session, clase) -> bool:
    """Actualiza un evento existente en Google Calendar."""
    if not clase.google_event_id:
        return False

    fin = clase.fecha + __import__('datetime').timedelta(minutes=60)

    body = {
        "summary": f"🏫 {clase.titulo} — {clase.grupo}",
        "description": (
            f"Clase de gestión emocional\n"
            f"Grupo: {clase.grupo}\n"
            f"Tema: {clase.tema or 'Sin especificar'}\n"
            f"Notas: {clase.notas or ''}\n\n"
            f"📱 Actualizado desde K.I.W.I."
        ),
        "start": {"dateTime": clase.fecha.isoformat(), "timeZone": "America/Bogota"},
        "end":   {"dateTime": fin.isoformat(),          "timeZone": "America/Bogota"},
    }

    result = _api_request(session, "PUT",
        f"/calendars/primary/events/{clase.google_event_id}", body)
    return result is not None


def eliminar_evento_google(session, google_event_id: str) -> bool:
    """Elimina un evento de Google Calendar."""
    if not google_event_id:
        return False
    result = _api_request(session, "DELETE",
        f"/calendars/primary/events/{google_event_id}")
    return True  # DELETE retorna 204 sin body


def listar_eventos_google(session, dias: int = 30) -> list:
    """
    Trae eventos de Google Calendar de los próximos N días.
    Útil para mostrar en el calendario de KIWI lo que ya existe en Google.
    """
    from datetime import datetime, timedelta
    ahora = datetime.now(tz.utc)
    hasta = ahora + timedelta(days=dias)

    params = urllib.parse.urlencode({
        "timeMin":    ahora.isoformat(),
        "timeMax":    hasta.isoformat(),
        "singleEvents": "true",
        "orderBy":    "startTime",
        "maxResults": "50",
    })

    result = _api_request(session, "GET", f"/calendars/primary/events?{params}")
    if not result:
        return []
    return result.get("items", [])


def desconectar_google(session) -> None:
    """Revoca el token y limpia la sesión."""
    token = session.get('google_access_token')
    if token:
        try:
            data = urllib.parse.urlencode({"token": token}).encode()
            req = urllib.request.Request(GOOGLE_REVOKE_URL, data=data, method="POST")
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass

    for key in ['google_access_token', 'google_refresh_token',
                'google_token_expires', 'google_connected']:
        session.pop(key, None)
    session.modified = True
