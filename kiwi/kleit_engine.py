"""
╔══════════════════════════════════════════════════════════════╗
║           K L E I T   —   Motor de Inteligencia Artificial  ║
║           K.I.W.I. · Colegio San Francisco de Asís          ║
╚══════════════════════════════════════════════════════════════╝

Motor de chat con Gemini (REST API directa) — historial completo.
Kleit responde exclusivamente con Gemini AI.
"""

import json
import logging
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════
# PROMPT MAESTRO DEL SISTEMA
# ══════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """
Eres Kleit, el asistente virtual de K.I.W.I., una plataforma educativa del
Colegio San Francisco de Asís (Cali, Colombia) diseñada para apoyar a docentes
de gestión emocional y bienestar psicológico.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTEXTO DE TU USUARIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- La docente trabaja con grupos de básica primaria y bachillerato.
- Los estudiantes son colombianos, contexto urbano, edades 6-17 años.
- Las clases duran entre 45 y 60 minutos.
- El enfoque pedagógico es: práctico, vivencial, basado en psicología positiva
  y neurociencia del aprendizaje socioemocional.
- La docente valora actividades originales, con pasos claros y que no requieran
  muchos materiales costosos.
- El lenguaje del colegio es español colombiano.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TU PERSONALIDAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Tono: amigable, cálido, profesional. Como un colega experto.
- Eres experto/a en SEL (Social Emotional Learning), psicología positiva,
  mindfulness educativo y pedagogía activa.
- Tienes memoria de toda la conversación: no repites lo que ya propusiste.
- Recuerdas el contexto: si la docente te pide variaciones o más detalles,
  trabajas sobre lo anterior.
- Si te hacen una pregunta (no piden actividades), responde con texto conversacional
  en el campo consejo_kleit y deja ideas vacío.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMATO DE RESPUESTA — SIEMPRE JSON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Responde ÚNICAMENTE con un objeto JSON válido. Sin texto extra, sin markdown.

Cuando pidan ACTIVIDADES (3 ideas):
{
  "nivel_detectado": "primaria | bachillerato | general",
  "categoria_emocional": "nombre de la categoría emocional",
  "consejo_kleit": "Tip personalizado de 2-3 oraciones para la docente",
  "ideas": [
    {
      "titulo": "Nombre creativo de la actividad 🎯",
      "descripcion": "Descripción breve y motivadora (2 oraciones)",
      "duracion_minutos": 45,
      "materiales": ["Material 1", "Material 2"],
      "pasos": [
        "Introducción (X min): descripción detallada",
        "Desarrollo (X min): descripción detallada",
        "Actividad principal (X min): descripción detallada",
        "Reflexión (X min): descripción detallada",
        "Cierre (X min): descripción detallada"
      ],
      "preguntas_reflexion": ["Pregunta 1 para el grupo", "Pregunta 2"],
      "indicador_logro": "Cómo saber si la actividad funcionó",
      "adaptacion_primaria": "Cómo simplificar para primaria",
      "adaptacion_bachillerato": "Cómo profundizar para bachillerato",
      "recursos_digitales": ["Recurso gratuito 1", "Recurso gratuito 2"]
    }
  ]
}

Cuando la docente haga una PREGUNTA o pida DETALLES (no nuevas actividades):
{
  "nivel_detectado": "general",
  "categoria_emocional": "",
  "consejo_kleit": "Tu respuesta conversacional completa aquí",
  "ideas": []
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REGLAS PEDAGÓGICAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Para PRIMARIA: actividades lúdicas, visuales, con movimiento corporal,
   metáforas simples, máximo 3 pasos principales.
2. Para BACHILLERATO: reflexión crítica, debate, análisis de situaciones
   reales, conexión con vida cotidiana y redes sociales.
3. SIEMPRE incluye un momento de cierre/reflexión de al menos 5 minutos.
4. Los materiales deben ser económicos y disponibles en un colegio colombiano.
5. Las 3 actividades deben ser DIFERENTES entre sí en metodología.
6. NUNCA repitas una actividad que ya aparezca en el historial de la conversación.
7. Cada nueva petición debe traer ideas completamente nuevas y originales.
8. Las actividades DEBEN estar DIRECTAMENTE relacionadas con el tema exacto pedido.
   Si piden "manejo del estrés", TODAS las actividades deben ser sobre manejo del estrés.
   No divagues ni generes actividades de temas distintos.
9. El campo consejo_kleit debe ser un tip pedagógico ESPECÍFICO y ÚNICO para el tema
   pedido en esta consulta. NUNCA empieces con frases genéricas como "¡Claro!",
   "¡Por supuesto!", "Aquí tienes...", "¡Excelente elección!" o similares.
   Ve directo al tip concreto sobre el tema solicitado.
10. Si el mensaje del usuario incluye "(Grupo objetivo: X)", usa esa información para
    adaptar las actividades al nivel del grupo pero NO la menciones en tu respuesta.
"""


# ══════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════════

def chat_con_kleit(mensajes_history: list, historial_global_titulos: list = None) -> dict:
    """
    Función principal del motor Kleit.

    Args:
        mensajes_history: Lista completa de mensajes de la conversación,
                          incluyendo el nuevo mensaje del usuario al final.
                          Formato: [{"role": "user"|"assistant", "content": str}, ...]
        historial_global_titulos: Títulos de TODAS las ideas usadas por la docente
                                   en cualquier sesión previa.

    Returns:
        dict con: ideas, nivel, categoria, consejo, fuente, raw
    """
    historial_global_titulos = historial_global_titulos or []

    resultado = _llamar_gemini(mensajes_history, historial_global_titulos)
    if resultado:
        resultado['fuente'] = 'gemini'
        return resultado

    # Gemini no respondió — informar al usuario
    logger.warning("Kleit: Gemini no disponible, no se generaron actividades.")
    return {
        'ideas': [],
        'nivel': 'general',
        'categoria': '',
        'consejo': (
            'En este momento no puedo conectarme al servicio de inteligencia artificial. '
            'Por favor verifica tu conexión a internet y vuelve a intentarlo en unos momentos.'
        ),
        'fuente': 'error',
    }


# ══════════════════════════════════════════════════════════════════
# LLAMADA A GEMINI — REST API DIRECTA (sin SDK, sin gRPC)
# ══════════════════════════════════════════════════════════════════

def _llamar_gemini(mensajes_history: list, historial_global: list) -> dict | None:
    """
    Llama a la API REST de Gemini directamente con urllib.
    No usa el SDK google-generativeai (que bloquea por gRPC/SSL en algunos entornos).
    """
    from django.conf import settings

    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        logger.info("Kleit: GEMINI_API_KEY no configurada.")
        return None

    model = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash')
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )

    # System prompt con historial de actividades ya usadas
    system_text = SYSTEM_PROMPT
    if historial_global:
        titulos_str = '\n'.join(f'  - {t}' for t in historial_global[:60])
        system_text += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ACTIVIDADES YA USADAS — OBLIGATORIO NO REPETIR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Las siguientes actividades ya fueron propuestas a esta docente en sesiones anteriores.
DEBES generar ideas COMPLETAMENTE NUEVAS. No uses el mismo nombre ni la misma dinámica:
{titulos_str}
"""

    # Convertir historial al formato de Gemini (role: user | model)
    contents = []
    for m in mensajes_history:
        role = 'user' if m['role'] == 'user' else 'model'
        contents.append({'role': role, 'parts': [{'text': m['content']}]})

    payload = {
        'system_instruction': {'parts': [{'text': system_text}]},
        'contents': contents,
        'generationConfig': {
            'response_mime_type': 'application/json',
            'temperature': 0.85,
        },
    }

    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())

        texto = data['candidates'][0]['content']['parts'][0]['text'].strip()
        # Limpiar markdown si Gemini lo añade igualmente
        if '```' in texto:
            parte = texto.split('```')[1]
            texto = parte[4:] if parte.startswith('json') else parte
        texto = texto.strip()

        datos = json.loads(texto)
        return {
            'ideas': datos.get('ideas', []),
            'nivel': datos.get('nivel_detectado', 'general'),
            'categoria': datos.get('categoria_emocional', ''),
            'consejo': datos.get('consejo_kleit', ''),
            'raw': texto,
        }

    except urllib.error.HTTPError as e:
        body_err = e.read().decode(errors='ignore')
        logger.error(f"Kleit Gemini HTTP {e.code}: {body_err[:300]}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Kleit Gemini JSON parse error: {e}")
        return None
    except Exception as e:
        logger.error(f"Kleit Gemini error: {type(e).__name__}: {e}")
        return None


# ══════════════════════════════════════════════════════════════════
# DETECTORES
# ══════════════════════════════════════════════════════════════════

def detectar_nivel(texto: str) -> str:
    g = texto.lower().strip()
    palabras_primaria = ['primaria', '1°', '2°', '3°', '4°', '5°',
                         'grado 1', 'grado 2', 'grado 3', 'grado 4', 'grado 5',
                         'primero', 'segundo', 'tercero', 'cuarto', 'quinto']
    palabras_bachillerato = ['bachillerato', '6°', '7°', '8°', '9°', '10°', '11°',
                              'grado 6', 'grado 7', 'grado 8', 'grado 9', 'grado 10', 'grado 11',
                              '6a', '7a', '8a', '9a', '10a', '11a',
                              'sexto', 'séptimo', 'octavo', 'noveno', 'décimo', 'once']
    if any(p in g for p in palabras_primaria):
        return 'primaria'
    if any(p in g for p in palabras_bachillerato):
        return 'bachillerato'
    return 'general'


def detectar_categoria(tema: str) -> str:
    t = tema.lower()
    categorias = {
        'autorregulación': ['estres', 'estrés', 'ansiedad', 'control', 'calma', 'respiracion',
                            'mindfulness', 'autorregulacion', 'pausa', 'impulso'],
        'emociones básicas': ['emocion', 'emociones', 'sentimientos', 'rabia', 'alegria',
                               'tristeza', 'miedo', 'asco', 'sorpresa'],
        'empatía y relaciones': ['empatia', 'relaciones', 'comunicacion', 'conflicto',
                                  'asertividad', 'limites', 'amistad', 'familia', 'escucha'],
        'identidad y autoestima': ['autoestima', 'identidad', 'autoconcepto', 'confianza',
                                    'valores', 'proposito', 'metas', 'yo'],
        'bienestar y gratitud': ['bienestar', 'gratitud', 'felicidad', 'positividad',
                                  'resiliencia', 'esperanza', 'optimismo'],
        'habilidades sociales': ['liderazgo', 'trabajo en equipo', 'colaboracion',
                                  'respeto', 'tolerancia', 'diversidad'],
        'salud mental digital': ['redes', 'digital', 'internet', 'tecnologia',
                                  'cyberbullying', 'pantallas', 'celular'],
        'duelo y pérdida': ['duelo', 'perdida', 'muerte', 'separacion', 'despedida', 'cambio'],
    }
    for categoria, palabras in categorias.items():
        if any(p in t for p in palabras):
            return categoria
    return 'gestión emocional general'


# ══════════════════════════════════════════════════════════════════
# COMPATIBILIDAD LEGACY
# ══════════════════════════════════════════════════════════════════

def generar_ideas(tema: str, grupo: str, historial_titulos: list = None,
                  historial_temas: list = None) -> dict:
    """Wrapper legacy que usa el nuevo motor de chat."""
    historial_titulos = historial_titulos or []
    contenido = f"Tema: {tema} | Grupo: {grupo}"
    if historial_titulos:
        contenido += f"\n⚠️ NO repitas estas actividades: {', '.join(historial_titulos[:20])}"
    resultado = chat_con_kleit(
        [{"role": "user", "content": contenido}],
        historial_titulos,
    )
    return resultado
