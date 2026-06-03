import json
import logging
import urllib.request
import urllib.error
from django.conf import settings

logger = logging.getLogger(__name__)


def enviar_email(destinatario: str, asunto: str, cuerpo: str) -> bool:
    """Envía un email via Resend API — HTTP directo, sin SMTP."""
    api_key = getattr(settings, 'RESEND_API_KEY', '')
    if not api_key:
        logger.warning('RESEND_API_KEY no configurada — email no enviado.')
        return False

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'KIWI <noreply@kiwi.com>')

    payload = json.dumps({
        'from': from_email,
        'to': [destinatario],
        'subject': asunto,
        'text': cuerpo,
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.resend.com/emails',
        data=payload,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            logger.info(f'Email enviado a {destinatario} via Resend — status {resp.status}')
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        logger.error(f'Resend HTTP {e.code} enviando a {destinatario}: {body}')
        return False
    except Exception as e:
        logger.error(f'Error enviando email a {destinatario}: {type(e).__name__}: {e}')
        return False
