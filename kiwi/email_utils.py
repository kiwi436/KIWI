import base64
import json
import logging
import urllib.request
import urllib.error
import urllib.parse
from django.conf import settings

logger = logging.getLogger(__name__)

GMAIL_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GMAIL_SEND_URL  = 'https://gmail.googleapis.com/gmail/v1/users/me/messages/send'


def _obtener_access_token(refresh_token: str) -> str | None:
    """Intercambia el refresh token por un access token."""
    data = urllib.parse.urlencode({
        'client_id':     getattr(settings, 'GOOGLE_CLIENT_ID', ''),
        'client_secret': getattr(settings, 'GOOGLE_CLIENT_SECRET', ''),
        'refresh_token': refresh_token,
        'grant_type':    'refresh_token',
    }).encode()
    req = urllib.request.Request(GMAIL_TOKEN_URL, data=data, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())['access_token']
    except Exception as e:
        logger.error(f'Gmail: error obteniendo access token: {e}')
        return None


def enviar_email(destinatario: str, asunto: str, cuerpo: str) -> bool:
    """Envía un email usando Gmail API con OAuth2."""
    from .models import ConfiguracionApp
    config = ConfiguracionApp.get()

    if not config.gmail_refresh_token:
        logger.warning('Gmail no autorizado — ve a /admin/gmail/conectar/ para autorizar.')
        return False

    access_token = _obtener_access_token(config.gmail_refresh_token)
    if not access_token:
        return False

    remitente = config.gmail_email or 'noreply@gmail.com'
    mensaje_raw = (
        f'From: KIWI <{remitente}>\r\n'
        f'To: {destinatario}\r\n'
        f'Subject: {asunto}\r\n'
        f'Content-Type: text/plain; charset=utf-8\r\n\r\n'
        f'{cuerpo}'
    )
    encoded = base64.urlsafe_b64encode(mensaje_raw.encode('utf-8')).decode('utf-8')
    payload = json.dumps({'raw': encoded}).encode('utf-8')

    req = urllib.request.Request(
        GMAIL_SEND_URL,
        data=payload,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            logger.info(f'Gmail: email enviado a {destinatario} — status {resp.status}')
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        logger.error(f'Gmail HTTP {e.code} enviando a {destinatario}: {body}')
        return False
    except Exception as e:
        logger.error(f'Gmail error enviando a {destinatario}: {e}')
        return False
