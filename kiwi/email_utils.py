import json
import logging
import urllib.request
import urllib.error
from django.conf import settings

logger = logging.getLogger(__name__)


def enviar_email(destinatario: str, asunto: str, cuerpo: str) -> bool:
    """Envía un email via Brevo (Sendinblue) API — HTTP directo, sin SMTP."""
    api_key = getattr(settings, 'BREVO_API_KEY', '')
    if not api_key:
        logger.warning('BREVO_API_KEY no configurada — email no enviado.')
        return False

    nombre_remitente = 'KIWI'
    email_remitente = getattr(settings, 'EMAIL_HOST_USER', 'noreply@kiwi.edu.co')

    payload = json.dumps({
        'sender': {'name': nombre_remitente, 'email': email_remitente},
        'to': [{'email': destinatario}],
        'subject': asunto,
        'textContent': cuerpo,
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.brevo.com/v3/smtp/email',
        data=payload,
        headers={
            'api-key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            logger.info(f'Email enviado a {destinatario} via Brevo — status {resp.status}')
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        logger.error(f'Brevo HTTP {e.code} enviando a {destinatario}: {body}')
        return False
    except Exception as e:
        logger.error(f'Error enviando email a {destinatario}: {type(e).__name__}: {e}')
        return False
