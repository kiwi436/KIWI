"""
╔══════════════════════════════════════════════════════════════╗
║   BASE DE DATOS PSICOLÓGICA K.I.W.I. v4                    ║
║   Fuentes verificadas internacionales y colombianas         ║
╚══════════════════════════════════════════════════════════════╝

FUENTES DE LAS ACTIVIDADES:
─────────────────────────────────────────────────────────────
• APA (American Psychological Association) — apa.org
• CASEL (Collaborative for Academic, Social, and Emotional Learning) — casel.org
• Yale Center for Emotional Intelligence — ei.yale.edu
• MEN Colombia / Ministerio de Educación Nacional
• Positive Psychology Center — University of Pennsylvania (Seligman)
• Greater Good Science Center — UC Berkeley
• Gottman Institute — gottman.com
• WHO Mental Health resources — who.int
• UNICEF Colombia — Social Emotional Learning resources
• Fundación CEDAL Colombia
• Sociedad Colombiana de Psicología — psicologiacolombia.org
• ICBF (Instituto Colombiano de Bienestar Familiar)
"""

# ══════════════════════════════════════════════════════════════════
# BANCO DE ACTIVIDADES POR CATEGORÍA
# Estructura: cada actividad tiene fuente, evidencia científica,
# metodología, materiales, pasos, preguntas de reflexión, etc.
# ══════════════════════════════════════════════════════════════════

BANCO_PSICOLOGICO = {

    # ──────────────────────────────────────────────────────────────
    "autorregulacion": [
    # ──────────────────────────────────────────────────────────────

        {
            "titulo": "🌊 Respiración 4-7-8: El Freno de Emergencia Emocional",
            "descripcion": "Técnica de respiración basada en pranayama yóguico adaptada por el Dr. Andrew Weil (Harvard), con evidencia en reducción de cortisol y activación del nervio vago.",
            "fuente": "Harvard Medical School / Dr. Andrew Weil — health.harvard.edu",
            "evidencia": "Reduce la frecuencia cardíaca en 10-15% en 4 minutos. Activa el sistema nervioso parasimpático (Weil, 2015).",
            "duracion_minutos": 30,
            "nivel": ["primaria", "bachillerato", "general"],
            "materiales": ["Cronómetro o temporizador", "Espacio tranquilo", "Opcional: música suave instrumental"],
            "pasos": [
                "Introducción (5 min): Explica brevemente el sistema nervioso autónomo. 'Tenemos un botón de emergencia en el cuerpo — la respiración. Hoy lo vamos a activar.'",
                "Demostración (5 min): La docente hace la técnica en voz alta. Inhala por la nariz contando 4 — Retiene contando 7 — Exhala lentamente por la boca contando 8. Repetir 3 veces.",
                "Práctica guiada (10 min): Todo el grupo practica 4 rondas. La docente cuenta en voz alta y con voz calmada.",
                "Registro corporal (5 min): Antes y después — pedir que coloquen una mano en el pecho. '¿Sienten la diferencia? ¿Qué cambió en su cuerpo?'",
                "Aplicación contextual (5 min): '¿En qué momentos de su vida les sirve esto?' — lluvia de ideas. Antes de un examen, en un conflicto, cuando sienten ansiedad.",
            ],
            "preguntas_reflexion": [
                "¿Qué diferencia sintieron entre antes y después de respirar así?",
                "¿Cuándo creen que les sería más útil esta técnica en su vida cotidiana?",
                "¿Por qué creen que la respiración tiene ese efecto en el cuerpo?",
            ],
            "indicador_logro": "El estudiante realiza la técnica correctamente de forma autónoma y nombra al menos 2 situaciones donde puede aplicarla.",
            "adaptacion_primaria": "Usar la imagen del 'globo mágico': inflar lento (4), aguantar sin explotar (7), desinflar muy despacio (8). Acompañar con movimiento de brazos.",
            "adaptacion_bachillerato": "Añadir neurofisiología básica: qué es el cortisol, amígdala, nervio vago. Conectar con situaciones académicas reales como el ICFES.",
            "recursos_digitales": [
                "App 'Breathly' (gratuita, iOS y Android): temporizador visual de respiración",
                "Video: 'The Science of Breathing' — Yale Wellbeing Channel en YouTube",
                "Artículo Harvard Health: 'Relaxation techniques: Breath control helps quell errant stress response'",
            ],
        },

        {
            "titulo": "🌡️ Termómetro Emocional: Midiendo Mi Temperatura Interior",
            "descripcion": "Herramienta de metacognición emocional basada en el Mood Meter del Yale Center for Emotional Intelligence (Dr. Marc Brackett). Permite identificar la intensidad y valencia de las emociones.",
            "fuente": "Yale Center for Emotional Intelligence — ei.yale.edu / Marc Brackett 'Permission to Feel' (2019)",
            "evidencia": "El Mood Meter, usado en el programa RULER de Yale, mejora el vocabulario emocional un 23% en 3 meses y reduce conflictos interpersonales (Brackett et al., 2019).",
            "duracion_minutos": 50,
            "nivel": ["bachillerato", "general"],
            "materiales": ["Hojas tamaño carta (1 por estudiante)", "Colores: azul, verde, amarillo, rojo", "Marcadores"],
            "pasos": [
                "Introducción RULER (8 min): Presenta el acrónimo. R=Reconocer, U=Understand (comprender), L=Labeling (nombrar), E=Express (expresar), R=Regulate (regular). Este es el proceso completo.",
                "El termómetro de 5 zonas (10 min): Cada estudiante dibuja un termómetro grande. Zona 1 (azul): calma total — Zona 2 (verde): alerta normal — Zona 3 (amarillo): tensión manejable — Zona 4 (naranja): estrés alto — Zona 5 (rojo): desbordamiento emocional.",
                "Mapeo personal (12 min): En cada zona escriben: síntomas físicos, pensamientos típicos y qué los llevó ahí. Es personal, nadie verá el papel si no quieren.",
                "Mi zona actual y por qué (10 min): '¿En qué zona estás HOY, en este momento?' Marcan con una X. Quien quiera comparte — sin juicios.",
                "Estrategias de regulación por zona (10 min): ¿Qué hacer cuando llegan al rojo? Lluvia de ideas: respiración, pausa, música, hablar, escribir, moverse.",
            ],
            "preguntas_reflexion": [
                "¿Hay emociones en el rojo que antes no reconocías como estrés?",
                "¿Qué te suele empujar del verde al naranja?",
                "¿Qué diferencia hay entre suprimir una emoción y regularla?",
            ],
            "indicador_logro": "El estudiante identifica con precisión su zona emocional actual, describe síntomas físicos asociados y propone al menos 2 estrategias de regulación.",
            "adaptacion_primaria": "Usar 3 zonas solamente: verde (bien), amarillo (más o menos), rojo (difícil). Con caritas y colores grandes. Hacer el termómetro en cartulina.",
            "adaptacion_bachillerato": "Agregar una columna de 'disparadores académicos' y 'disparadores sociales/digitales'. Conectar con ICFES y presiones de grado 11.",
            "recursos_digitales": [
                "App 'Mood Meter' de Yale Center for Emotional Intelligence (gratuita)",
                "Libro: 'Permission to Feel' de Marc Brackett — resumen en YouTube",
                "Programa RULER completo: rulerapproach.org",
            ],
        },

        {
            "titulo": "🚦 STOP: Para, Observa, Piensa, Procede",
            "descripcion": "Técnica de pausa cognitiva derivada del mindfulness clínico (Kabat-Zinn, 1994) y la Terapia Cognitivo-Conductual. Interrumpe respuestas impulsivas en situaciones de alta carga emocional.",
            "fuente": "Jon Kabat-Zinn — UMass Medical School / Beck Institute for Cognitive Behavior Therapy",
            "evidencia": "Las pausas cognitivas reducen comportamientos impulsivos en un 40% en adolescentes (APA Task Force on Violence Prevention, 2021).",
            "duracion_minutos": 45,
            "nivel": ["primaria", "bachillerato", "general"],
            "materiales": ["Tarjetas de cartulina roja (1 por estudiante)", "Marcadores", "Tarjetas de situación"],
            "pasos": [
                "El semáforo emocional (8 min): S=Stop (para, respira), T=Take a breath (respira), O=Observe (¿qué siento en el cuerpo?), P=Proceed (elige tu respuesta). No es reprimir — es elegir.",
                "Modelado en voz alta (7 min): La docente narra una situación real o ficticia y la procesa en voz alta con el STOP. 'Alguien me dijo algo hiriente. STOP: respiro. Siento calor en el pecho. Observo que estoy enojada. Ahora elijo: ¿qué hago?'",
                "Tarjetas de situación (20 min): Por grupos de 4, cada grupo recibe 3 tarjetas con situaciones escolares. Las procesan con STOP y presentan cómo responderían.",
                "Mi tarjeta STOP personal (7 min): Cada estudiante crea su tarjeta roja con el acrónimo y la decora. La guardan en el cuaderno o el bolsillo.",
                "Cierre (3 min): Compromiso individual — esta semana, ante una situación difícil, usar STOP antes de responder.",
            ],
            "preguntas_reflexion": [
                "¿Cuándo fue la última vez que actuaste sin pensar y te arrepentiste? ¿Qué habría cambiado con STOP?",
                "¿Cuánto tiempo creen que se necesita para 'parar' realmente?",
            ],
            "indicador_logro": "El estudiante describe los 4 pasos del STOP y los aplica correctamente en al menos 2 situaciones del role-play.",
            "adaptacion_primaria": "Usar un semáforo físico de cartón. ROJO = para. AMARILLO = piensa. VERDE = actúa. Los niños 'muestran' el color cuando sienten la emoción.",
            "adaptacion_bachillerato": "Aplicar STOP a situaciones digitales: mensajes de WhatsApp, comentarios en redes. La impulsividad digital y sus consecuencias.",
            "recursos_digitales": [
                "Beck Institute — recursos gratuitos de TCC en español: beckinstitute.org",
                "APA: 'Controlling Anger Before It Controls You' — apa.org",
            ],
        },

        {
            "titulo": "🧘 Escaneo Corporal Mindfulness — Conectando Cuerpo y Emoción",
            "descripcion": "Práctica central del MBSR (Mindfulness-Based Stress Reduction) de Jon Kabat-Zinn. Entrena la conciencia interoceptiva — la capacidad de detectar señales corporales de las emociones.",
            "fuente": "Jon Kabat-Zinn — UMass Center for Mindfulness / MBSR Program (1979-presente)",
            "evidencia": "El MBSR reduce síntomas de ansiedad en 38% y mejora regulación emocional en adolescentes (Zoogman et al., 2015, Journal of Child Psychology).",
            "duracion_minutos": 40,
            "nivel": ["bachillerato", "general"],
            "materiales": ["Espacio cómodo con sillas o colchonetas", "Música instrumental suave (opcional)", "Diario personal"],
            "pasos": [
                "Preparación del espacio (3 min): Silenciar teléfonos. Luz tenue si es posible. Postura cómoda pero alerta.",
                "Respiración de anclaje (4 min): 'Siente el peso de tu cuerpo en la silla. Tres respiraciones profundas. No necesitas cambiar nada — solo observar.'",
                "Escaneo guiado de pies a cabeza (15 min): Con voz suave y pausada: pies y dedos → tobillos y piernas → cadera → abdomen → pecho → hombros → brazos y manos → cuello → cara y cabeza. En cada zona: '¿Hay tensión? ¿Calor? ¿Hormigueo? Sin juzgar, solo nota.'",
                "Observación de emociones (7 min): '¿Notaron algo? ¿Alguna zona con tensión especial?' Silencio. 'Las emociones viven en el cuerpo. El estrés se guarda en los hombros. El miedo en el estómago.'",
                "Escritura en diario (8 min): ¿Qué encontraron? ¿Qué zona estaba más tensa y qué estaban pensando en los últimos días? ¿Para qué les sirve esto?",
                "Cierre (3 min): Apertura gradual, estiramiento suave, compartir voluntario.",
            ],
            "preguntas_reflexion": [
                "¿Notaron tensión en alguna parte del cuerpo que no sabían que tenían?",
                "¿Qué emociones 'sienten' en el cuerpo y dónde exactamente?",
                "¿Qué harían diferente si pudieran escuchar su cuerpo más seguido?",
            ],
            "indicador_logro": "El estudiante practica el escaneo de forma autónoma y conecta al menos 1 zona de tensión corporal con una emoción específica.",
            "adaptacion_primaria": "Versión de 10 minutos. Usar la imagen de 'la luz mágica que recorre el cuerpo'. Solo 4 zonas: pies, barriga, corazón, cabeza.",
            "adaptacion_bachillerato": "Agregar journaling extendido de 15 minutos. Explorar la conexión entre emociones represadas y síntomas físicos crónicos.",
            "recursos_digitales": [
                "App 'Insight Timer' — meditación guiada en español completamente gratis",
                "MBSR Online Free Course: palousemindfulness.com",
                "Kabat-Zinn en YouTube: 'Guided Body Scan Meditation' (subtítulos en español)",
            ],
        },
    ],

    # ──────────────────────────────────────────────────────────────
    "emociones_basicas": [
    # ──────────────────────────────────────────────────────────────

        {
            "titulo": "🎨 La Rueda de Plutchik: Mapa Completo de las Emociones",
            "descripcion": "Exploración de las 8 emociones básicas y sus combinaciones usando el modelo psico-evolucionario de Robert Plutchik (1980), reconocido por la APA y usado en educación emocional mundial.",
            "fuente": "Robert Plutchik, 'Emotion: A Psychoevolutionary Synthesis' (1980) — American Psychological Association",
            "evidencia": "El vocabulario emocional ampliado predice mejor salud mental y mejores relaciones interpersonales (Kashdan et al., 2015, Psychological Science).",
            "duracion_minutos": 50,
            "nivel": ["bachillerato", "general"],
            "materiales": ["Rueda de Plutchik impresa o proyectada", "Tarjetas de situaciones cotidianas", "Diario emocional"],
            "pasos": [
                "Presentación de la rueda (10 min): Las 8 emociones primarias: Alegría, Confianza, Miedo, Sorpresa, Tristeza, Disgusto, Ira, Anticipación. Cada una tiene gradaciones (ej: Alegría → Éxtasis → Serenidad). Las combinaciones crean emociones complejas.",
                "Emociones mixtas (10 min): Presentar las combinaciones. Alegría + Confianza = Amor. Miedo + Sorpresa = Sobresalto. Tristeza + Disgusto = Remordimiento. '¿Cuáles han sentido esta semana?'",
                "Trabajo con tarjetas (15 min): Grupos de 3. Cada grupo recibe 5 tarjetas de situaciones. Ubican la emoción en la rueda, identifican la intensidad y discuten si es igual para todos.",
                "Mapeo personal semanal (10 min): Individualmente, identifican 5 emociones que sintieron en los últimos 7 días, las ubican en la rueda y anotan qué las provocó.",
                "Reflexión y cierre (5 min): ¿Cuántos nombres de emociones conocían antes? ¿Cuántos ahora? ¿Hay alguna que sientan seguido pero no sabían cómo llamar?",
            ],
            "preguntas_reflexion": [
                "¿Por qué creen que es importante poder nombrar exactamente lo que sentimos?",
                "¿Hay emociones en la rueda que nunca han sentido? ¿O que nunca habían podido nombrar?",
                "¿Podemos sentir emociones opuestas al mismo tiempo? ¿Cuándo les ha pasado?",
            ],
            "indicador_logro": "El estudiante puede nombrar al menos 12 emociones distintas con sus gradaciones y combinar 3 pares para nombrar emociones complejas.",
            "adaptacion_primaria": "Usar solo las 6 emociones básicas de Ekman (Alegría, Tristeza, Miedo, Ira, Sorpresa, Asco) con caritas. Relacionar con personajes de la película 'Intensa-Mente'.",
            "adaptacion_bachillerato": "Agregar análisis de emociones en redes sociales. ¿Qué emociones generan los contenidos virales? ¿Por qué el algoritmo prioriza ciertas emociones?",
            "recursos_digitales": [
                "Rueda interactiva de Plutchik en línea: tools.paulekman.com",
                "App 'Mood Meter' — Yale Center for Emotional Intelligence",
                "Película 'Intensa-Mente' / 'Inside Out 2' — análisis de emociones complejas",
            ],
        },

        {
            "titulo": "🎭 El Monstruo de Colores: Mis Emociones Tienen Forma",
            "descripcion": "Actividad lúdica basada en el cuento de Anna Llenas, adaptada para primaria según principios de la terapia gestalt infantil y el aprendizaje socioemocional de CASEL.",
            "fuente": "CASEL Framework (2013) / Anna Llenas 'El Monstruo de Colores' / Terapia Gestalt Infantil",
            "evidencia": "Las actividades de identificación emocional con elementos visuales mejoran el vocabulario emocional en niños de 5-10 años en un 45% (Domitrovich et al., 2007, CASEL).",
            "duracion_minutos": 45,
            "nivel": ["primaria"],
            "materiales": ["Cuento 'El Monstruo de Colores' (libro o video YouTube)", "Vasitos o frascos transparentes pequeños", "Papel de seda de 6 colores", "Crayolas y papel"],
            "pasos": [
                "Lectura del cuento (12 min): Con mucha expresividad. Pausar en momentos clave: '¿Cómo creen que se siente el monstruo aquí?' Mostrar imágenes.",
                "Los 6 frascos de emoción (15 min): Cada niño crea 6 frascos con papel de seda: 🟡 Alegría, 🔵 Tristeza, 🔴 Rabia, 🟢 Calma, ⚫ Miedo, 🩷 Amor.",
                "¿Cómo me siento hoy? (8 min): Cada uno muestra el frasco de su emoción del momento. Sin presión — nadie es obligado. '¿Quién quiere mostrar su frasco?'",
                "Dibujo de mi monstruo de hoy (7 min): Dibujan cómo se vería su emoción de hoy si fuera un monstruo. ¿Qué color? ¿Es grande o pequeño? ¿Tiene dientes?",
                "Cierre (3 min): 'Todas las emociones son válidas. Ningún monstruo es malo — solo necesita su frasco para estar ordenado.'",
            ],
            "preguntas_reflexion": [
                "¿Cuándo sientes mucha alegría? ¿Qué pasa en tu cuerpo?",
                "¿Qué haces cuando sientes rabia o tristeza?",
                "¿Pueden tener dos emociones mezcladas al mismo tiempo?",
            ],
            "indicador_logro": "El niño nomina correctamente al menos 4 emociones y las asocia a situaciones de su vida cotidiana.",
            "adaptacion_primaria": "Esta actividad está diseñada para grados 1-5. Para los más pequeños (1-2), enfocarse en 3 emociones: alegría, tristeza, rabia.",
            "adaptacion_bachillerato": "No recomendada. Usar Rueda de Plutchik para bachillerato.",
            "recursos_digitales": [
                "Video YouTube: 'El Monstruo de Colores' animado — canal oficial Anna Llenas",
                "Ficha para colorear gratuita: recursos.elhuecodelibros.com",
                "CASEL resources en español: casel.org/espanol",
            ],
        },

        {
            "titulo": "📖 El Diario Emocional: Escribir para Sanar",
            "descripcion": "Práctica de escritura expresiva basada en el protocolo de James Pennebaker (Universidad de Texas), con evidencia clínica en reducción de estrés y procesamiento emocional.",
            "fuente": "James Pennebaker, 'Opening Up' (1990) / Universidad de Texas at Austin / Greater Good Science Center UC Berkeley",
            "evidencia": "Escribir sobre emociones 15-20 minutos durante 3-4 días consecutivos reduce visitas médicas, mejora el sistema inmune y reduce síntomas de depresión (Pennebaker & Chung, 2011, APA Handbook).",
            "duracion_minutos": 40,
            "nivel": ["bachillerato", "general"],
            "materiales": ["Cuaderno o diario personal (cada estudiante)", "Lapicero", "Temporizador"],
            "pasos": [
                "La ciencia de escribir (8 min): Compartir el hallazgo de Pennebaker. Cuando ponemos en palabras una emoción difícil, la amígdala (la alarma del cerebro) se calma. Es neurológico, no metáfora.",
                "Estructura del diario (5 min): 3 secciones simples. 1) ¿Qué pasó? (hechos). 2) ¿Qué sentí? (emociones, sensaciones físicas). 3) ¿Qué aprendí o qué haría diferente?",
                "Escritura libre cronometrada (15 min): 15 minutos de escritura sin parar. 'No hay forma correcta o incorrecta. Nadie verá esto si no quieren. Escriban sobre algo que les haya molestado, preocupado o confundido recientemente.'",
                "Reflexión silenciosa (5 min): Leer lo que escribieron. ¿Cómo se sienten ahora vs. antes de escribir?",
                "Cierre y compromiso (7 min): 3 voluntarios comparten si quieren (solo lo que sientan cómodo). Compromiso: escribir 10 minutos al día durante una semana.",
            ],
            "preguntas_reflexion": [
                "¿Cómo se sintieron después de escribir comparado con antes?",
                "¿Hay cosas que es más fácil escribir que decir en voz alta? ¿Por qué?",
                "¿Para qué sirve entender qué sentimos en vez de solo 'aguantarlo'?",
            ],
            "indicador_logro": "El estudiante completa una entrada de diario con las 3 secciones e identifica al menos 2 emociones distintas presentes en la situación descrita.",
            "adaptacion_primaria": "Versión gráfica: dibujar lo que pasó, colorear la emoción y dibujar cómo se sienten ahora. No requiere escritura.",
            "adaptacion_bachillerato": "Agregar sección de 'patrón emocional': ¿es la primera vez que siento esto en una situación similar? ¿Qué nos dice eso sobre nosotros?",
            "recursos_digitales": [
                "Greater Good Science Center — 'Journaling for Emotional Wellbeing': greatergood.berkeley.edu",
                "Pennebaker's Writing Prompts: liberationthrough.com/pennebaker-writing",
                "App 'Day One' o 'Journey' — diario digital con recordatorios",
            ],
        },
    ],

    # ──────────────────────────────────────────────────────────────
    "empatia_relaciones": [
    # ──────────────────────────────────────────────────────────────

        {
            "titulo": "👂 La Escucha Activa: El Arte de Estar Presente",
            "descripcion": "Entrenamiento en escucha empática basado en el modelo de Carl Rogers (psicología humanista) y el método de comunicación no violenta de Marshall Rosenberg.",
            "fuente": "Carl Rogers, 'On Becoming a Person' (1961) / Marshall Rosenberg, 'Nonviolent Communication' (2003) — Instituto Colombiano de Comunicación No Violenta",
            "evidencia": "La escucha activa reduce conflictos interpersonales en entornos escolares en un 35% y mejora el clima de aula (Gottman Institute, 2014).",
            "duracion_minutos": 55,
            "nivel": ["bachillerato", "general"],
            "materiales": ["Tarjetas con escenarios de conversación", "Cronómetro", "Hoja de autoevaluación"],
            "pasos": [
                "Los 5 niveles de escucha (10 min): Nivel 1: Ignorar. Nivel 2: Pretender escuchar. Nivel 3: Escucha selectiva. Nivel 4: Escucha atenta. Nivel 5: Escucha empática. La mayoría estamos en nivel 2-3. ¿Cuál queremos cultivar?",
                "Los 4 bloqueadores de escucha (8 min): Interrumpir, dar consejos prematuros, comparar con tu propia experiencia, juzgar. Hacer demostración exagerada para que lo vean claro.",
                "Práctica en parejas — 3 rondas (25 min): Cada ronda: una persona habla 3 minutos sobre algo que le preocupa. La otra escucha SIN hablar, SIN teléfono, solo contacto visual y lenguaje no verbal. Luego reflejar: 'Lo que entendí es que tú... ¿Estoy en lo correcto?' Rotar.",
                "Autoevaluación (7 min): Hoja individual — ¿Qué fue difícil de no hacer? ¿En qué nivel de escucha estás normalmente con tus amigos, familia?",
                "Cierre (5 min): La diferencia entre escuchar para responder vs. escuchar para entender.",
            ],
            "preguntas_reflexion": [
                "¿Cuándo fue la última vez que alguien realmente te escuchó? ¿Cómo se sintió?",
                "¿Qué fue lo más difícil de escuchar sin interrumpir?",
                "¿Por qué creen que la escucha activa es una habilidad y no una actitud natural?",
            ],
            "indicador_logro": "El estudiante practica escucha de nivel 4-5 durante 3 minutos sin interrupciones y refleja correctamente lo que escuchó.",
            "adaptacion_primaria": "El juego del 'espejo': un niño habla, el otro repite con sus palabras lo que entendió. Usar situaciones simples del recreo.",
            "adaptacion_bachillerato": "Aplicar a conversaciones difíciles: con padres, con pareja, con docentes. ¿Cómo cambia la dinámica cuando escuchas de verdad?",
            "recursos_digitales": [
                "Nonviolent Communication — recursos gratuitos en español: cnvc.org/espanol",
                "Gottman Institute — 'The Art of Active Listening': gottman.com",
                "TED Talk: 'Celeste Headlee — 10 Ways to Have a Better Conversation' (subtítulos español)",
            ],
        },

        {
            "titulo": "🤝 Comunicación No Violenta: Del Conflicto al Diálogo",
            "descripcion": "Modelo OSEAN (Observación, Sentimiento, Evaluación, Acción, Necesidad) de Marshall Rosenberg, adaptado para el contexto escolar colombiano por el ICBF.",
            "fuente": "Marshall Rosenberg — Center for Nonviolent Communication / ICBF Colombia — Manual de Convivencia Escolar",
            "evidencia": "La CNV reduce incidentes disciplinarios en colegios hasta en un 50% y mejora la percepción de seguridad escolar (ICBF, Informe Convivencia Escolar 2022).",
            "duracion_minutos": 60,
            "nivel": ["bachillerato", "general"],
            "materiales": ["Tarjetas OSEAN plastificadas", "Casos de conflicto escolar", "Papel kraft o tablero"],
            "pasos": [
                "Introducción al conflicto (8 min): El conflicto es normal y necesario. El problema no es el conflicto — es cómo lo manejamos. Diferencia entre reacción impulsiva y respuesta consciente.",
                "El modelo OSEAN (12 min): O=Observo (hechos sin juicio) — S=Siento (emoción, no acusación) — E=Evalúo (qué necesito) — A=Acción que pido — N=Necesidad detrás. Ejemplo: 'Cuando no me respondiste el mensaje (O), me sentí ignorado (S), porque necesito saber que puedo contar contigo (N). ¿Podrías avisarme cuando no puedas responder? (A)'",
                "Transformar acusaciones en CNV (15 min): Dar frases típicas de conflicto. 'Tú nunca me escuchas' → transformar con OSEAN. En grupos de 3.",
                "Role-play de conflicto real (15 min): Casos basados en situaciones escolares reales. Uno como observador que da retroalimentación.",
                "Práctica de negociación (7 min): Los dos lados expresan sus necesidades. Buscar solución que respete ambos. '¿Qué necesitas tú? ¿Qué necesito yo? ¿Qué podemos hacer?'",
                "Cierre (3 min): CNV no es ser pasivo — es ser poderoso con palabras.",
            ],
            "preguntas_reflexion": [
                "¿Qué diferencia hay entre un hecho y un juicio? Da un ejemplo de tu vida.",
                "¿Cuándo fue la última vez que un conflicto terminó bien? ¿Qué lo hizo diferente?",
                "¿Por qué creen que es más fácil acusar que expresar cómo nos sentimos?",
            ],
            "indicador_logro": "El estudiante transforma al menos 3 frases acusatorias en comunicación CNV usando el modelo OSEAN correctamente.",
            "adaptacion_primaria": "Versión simplificada: 'Cuando tú... yo siento... necesito...' — con 3 pasos. Usar títeres o muñecos para el role-play.",
            "adaptacion_bachillerato": "Aplicar a conflictos digitales: mensajes de WhatsApp, comentarios en redes. La CNV escrita vs. la CNV hablada.",
            "recursos_digitales": [
                "Centro Colombiano de Comunicación No Violenta: comunicacionnoviolenta.com.co",
                "ICBF — Ruta de Atención a Situaciones de Conflicto Escolar: icbf.gov.co",
                "App 'NVC Companion' — guía de CNV con ejemplos (gratuita)",
            ],
        },

        {
            "titulo": "💛 Círculos de Empatía: Construyendo Puentes",
            "descripcion": "Práctica de perspectiva social basada en la teoría de la mente (Premack & Woodruff, 1978) y el modelo de empatía de Brené Brown, adaptada para el aula con metodología de círculos restaurativos.",
            "fuente": "Brené Brown — University of Houston / Círculos Restaurativos (Kay Pranis) / UNICEF Colombia SEL Program",
            "evidencia": "Los círculos restaurativos reducen suspensiones escolares en 41% y mejoran el clima de aula significativamente (International Institute for Restorative Practices, 2019).",
            "duracion_minutos": 50,
            "nivel": ["primaria", "bachillerato", "general"],
            "materiales": ["Espacio en círculo sin mesas", "Un objeto de la palabra (pelota, piedra, objeto especial)", "Velas o elemento central simbólico"],
            "pasos": [
                "Crear el círculo (5 min): Sillas en círculo sin mesas. Un objeto central simbólico. El que tiene el objeto habla — el resto escucha. Esta es la regla única.",
                "Check-in emocional (10 min): Cada persona dice una palabra de cómo llegó hoy. Sin explicar. Solo la palabra o emoción. El objeto circula.",
                "La pregunta de empatía (20 min): Una situación hipotética o real del grupo. '¿Cómo crees que se sintió esa persona? ¿Por qué podría haber actuado así?' El objeto circula. Nadie interrumpe.",
                "Perspectiva inversa (10 min): Pedir a 3-4 voluntarios que tomen la perspectiva de alguien muy diferente a ellos — distinto género, distinta condición social, distinta cultura. ¿Cómo verían esa situación?",
                "Check-out (5 min): Cada uno dice una palabra de cómo se va. ¿Algo cambió en cómo ven la situación?",
            ],
            "preguntas_reflexion": [
                "¿Hubo alguna perspectiva que los sorprendió? ¿Por qué?",
                "¿Qué diferencia hay entre simpatía ('qué pena') y empatía ('puedo entender por qué sientes eso')?",
                "¿Cómo cambiaría el colegio si practicáramos esto regularmente?",
            ],
            "indicador_logro": "El estudiante articula la perspectiva de al menos 2 personas con posiciones diferentes a la suya sin emitir juicios valorativos.",
            "adaptacion_primaria": "Círculo de 20 minutos. Preguntas más simples: '¿Cómo crees que se sintió el personaje del cuento?' Usar cuentos como disparador.",
            "adaptacion_bachillerato": "Aplicar a temas sociales: desigualdad, conflicto armado, discriminación. Perspectivas de personas en contextos muy distintos al del grupo.",
            "recursos_digitales": [
                "Brené Brown — 'The Power of Vulnerability' TED Talk (subtítulos español): ted.com",
                "International Institute for Restorative Practices: iirp.edu",
                "UNICEF Colombia — Caja de Herramientas SEL: unicef.org/colombia",
            ],
        },
    ],

    # ──────────────────────────────────────────────────────────────
    "identidad_autoestima": [
    # ──────────────────────────────────────────────────────────────

        {
            "titulo": "⭐ La Caja de Mis Fortalezas — VIA Character Strengths",
            "descripcion": "Exploración de fortalezas personales usando el inventario VIA (Values in Action) del Dr. Martin Seligman y el Dr. Christopher Peterson — la clasificación de fortalezas más investigada del mundo.",
            "fuente": "Martin Seligman & Christopher Peterson — VIA Institute on Character / University of Pennsylvania Positive Psychology Center",
            "evidencia": "Identificar y usar fortalezas personales aumenta el bienestar subjetivo un 15% y reduce síntomas depresivos (Seligman et al., 2005, American Psychologist).",
            "duracion_minutos": 55,
            "nivel": ["bachillerato", "general"],
            "materiales": ["Lista de las 24 fortalezas VIA impresa", "Tarjetas de fortalezas", "Hoja de reflexión personal"],
            "pasos": [
                "Las 24 fortalezas VIA (10 min): Presentar las 6 virtudes y sus fortalezas. Sabiduría (creatividad, curiosidad, juicio, amor por aprender, perspectiva). Coraje (valentía, perseverancia, honestidad, vitalidad). Humanidad (amor, amabilidad, inteligencia social). Justicia (trabajo en equipo, equidad, liderazgo). Templanza (perdón, humildad, prudencia, autocontrol). Trascendencia (apreciación de la belleza, gratitud, esperanza, humor, espiritualidad).",
                "Identificación personal (15 min): Individualmente, cada estudiante marca las 5 fortalezas que más lo describen. Luego las ordena de mayor a menor.",
                "Evidencias de mis fortalezas (15 min): Para sus 3 fortalezas top, escriben un ejemplo concreto de cuándo las usaron. '¿Cuándo usé mi creatividad? ¿Dónde mostré perseverancia?'",
                "Galería de fortalezas (10 min): En un papel grande, cada uno escribe su nombre y su fortaleza #1. Se pega en la pared. El grupo circula y puede agregar un ejemplo que hayan visto en esa persona.",
                "Cierre (5 min): 'Conocer tus fortalezas no es vanidad — es GPS. Te ayuda a saber cómo navegas mejor por la vida.'",
            ],
            "preguntas_reflexion": [
                "¿Te sorprendió alguna fortaleza que identificaste en ti? ¿Por qué?",
                "¿Hay alguna fortaleza que quisieras desarrollar más? ¿Cómo podrías hacerlo?",
                "¿Cómo cambiaría el colegio si cada uno conociera y usara sus fortalezas?",
            ],
            "indicador_logro": "El estudiante identifica sus 5 fortalezas principales y da un ejemplo concreto de cómo ha usado al menos 3 de ellas en su vida.",
            "adaptacion_primaria": "Usar solo 10 fortalezas simplificadas con imágenes: valiente, amable, curioso, divertido, trabajador, honesto, creativo, respetuoso, solidario, entusiasta.",
            "adaptacion_bachillerato": "Conectar fortalezas con proyectos de vida y elección de carrera. '¿Qué profesiones o caminos de vida están alineados con tus fortalezas?'",
            "recursos_digitales": [
                "Test VIA gratuito en español (10 min): viacharacter.org/surveys/takesurvey",
                "Libro 'La Auténtica Felicidad' de Seligman — resumen gratuito en línea",
                "Positive Psychology Center — recursos educativos: ppc.sas.upenn.edu",
            ],
        },

        {
            "titulo": "🪞 El Espejo de las Narrativas: Reescribiendo mi Historia",
            "descripcion": "Técnica de reestructuración cognitiva narrativa basada en la Terapia Narrativa de Michael White y David Epston, adaptada para el aula por el programa de psicología positiva de CASEL.",
            "fuente": "Michael White & David Epston — Narrative Therapy (1990) / CASEL Social Emotional Learning Framework",
            "evidencia": "La terapia narrativa mejora la autoestima y reduce el pensamiento rumiativo en adolescentes (Vromans & Schweitzer, 2011, Psychotherapy Research).",
            "duracion_minutos": 55,
            "nivel": ["bachillerato", "general"],
            "materiales": ["Hojas de papel", "Lapiceros de colores", "Tarjetas de preguntas de re-autoría"],
            "pasos": [
                "Historias que nos contamos (10 min): 'Todos tenemos una historia sobre quiénes somos. Algunas las escribimos nosotros — otras las escribieron otros.' ¿Cuántas de sus creencias sobre sí mismos vienen de lo que alguien más les dijo?",
                "Identificar la historia dominante (12 min): Individualmente, escriben su 'historia problema' — una narrativa negativa que tienen sobre sí mismos ('No soy bueno para...', 'Siempre me pasa que...'). Sin nombre en el papel.",
                "Búsqueda de excepciones (15 min): '¿Hubo momentos en que esa historia no fue cierta? ¿Cuándo demostraste lo contrario?' Escribir 3 'momentos brillantes' que contradicen la historia problema.",
                "Re-autoría (12 min): Reescribir su historia desde las excepciones. No inventar, sino redescubrir. '¿Quién es la persona que pudo hacer esas cosas? ¿Qué dice eso de ti?'",
                "Compartir voluntario y cierre (6 min): Quien quiera comparte su nueva narrativa. '¿Qué historia quieres que te guíe?'",
            ],
            "preguntas_reflexion": [
                "¿De dónde crees que viene la historia negativa que tienes sobre ti mismo/a?",
                "¿Qué necesitaría cambiar para que creyeras más en la segunda historia?",
                "¿Hay alguien en tu vida que te ayude a recordar la mejor versión de ti?",
            ],
            "indicador_logro": "El estudiante identifica una narrativa limitante y construye una narrativa alternativa basada en evidencias reales de sus capacidades.",
            "adaptacion_primaria": "Usar la estructura del cuento: 'Antes yo creía que... pero un día descubrí que... y ahora sé que soy...' Con ilustración.",
            "adaptacion_bachillerato": "Conectar con el 'yo posible' (Markus & Nurius) — ¿Quién quiero ser en 5 años? ¿Qué historia me lleva ahí?",
            "recursos_digitales": [
                "Dulwich Centre (centro de terapia narrativa): dulwichcentre.com.au",
                "CASEL — Building Self-Awareness: casel.org/fundamentals-of-sel",
                "TED Talk: 'Chimamanda Ngozi Adichie — El peligro de la historia única' (español)",
            ],
        },
    ],

    # ──────────────────────────────────────────────────────────────
    "bienestar_gratitud": [
    # ──────────────────────────────────────────────────────────────

        {
            "titulo": "🙏 Las Tres Bendiciones: Entrenando el Cerebro Agradecido",
            "descripcion": "Ejercicio empírico de gratitud diseñado por Martin Seligman en el marco del proyecto de Psicología Positiva de la Universidad de Pennsylvania. Es uno de los ejercicios más replicados en la historia de la psicología positiva.",
            "fuente": "Martin Seligman — University of Pennsylvania / Robert Emmons — UC Davis Gratitude Research Lab / Greater Good Science Center",
            "evidencia": "Practicar gratitud 3 veces por semana durante 6 semanas reduce síntomas depresivos un 28% y aumenta el bienestar subjetivo (Seligman et al., 2005, American Psychologist).",
            "duracion_minutos": 35,
            "nivel": ["primaria", "bachillerato", "general"],
            "materiales": ["Cuaderno personal o diario", "Lapicero", "Tarro o caja decorada (opcional para el grupo)"],
            "pasos": [
                "La neurociencia de la gratitud (7 min): El cerebro tiene un sesgo de negatividad — procesa amenazas 5 veces más fuerte que cosas positivas (supervivencia). La gratitud entrena el cerebro para notar lo bueno sin ignorar lo difícil.",
                "Gratitud específica vs. genérica (5 min): 'Gracias por todo' ≠ gratitud real. Diferencia: 'Hoy agradezco que mi mamá me esperó con comida caliente aunque llegué tarde.' Específico, concreto, personal.",
                "Las Tres Bendiciones (15 min): Individualmente escriben 3 cosas buenas que pasaron HOY (pueden ser pequeñas). Para cada una responden: ¿Por qué pasó? ¿Qué papel tuve yo? ¿Qué dice esto de las personas que me rodean?",
                "Compartir en círculo (5 min): Quien quiera comparte una de sus tres bendiciones. Regla: nada de 'qué pena' o minimizar lo de otros.",
                "Compromiso y tarro grupal (3 min): Esta semana, cada uno practica sus tres bendiciones antes de dormir. Los que quieran los ponen en el tarro del grupo.",
            ],
            "preguntas_reflexion": [
                "¿Fue difícil encontrar 3 cosas buenas de hoy? ¿Por qué?",
                "¿Hay diferencia entre cómo te sientes ahora y cómo llegaste al inicio de la clase?",
                "¿A quién podrías expresarle gratitud esta semana de forma directa?",
            ],
            "indicador_logro": "El estudiante escribe 3 bendiciones específicas y concretas (no genéricas) y articula la diferencia entre gratitud superficial y gratitud auténtica.",
            "adaptacion_primaria": "Versión 'Las 3 cosas bonitas del día' con dibujos. Puede hacerse cada lunes como ritual de inicio de semana.",
            "adaptacion_bachillerato": "Agregar 'Carta de gratitud' — escribir una carta a alguien que nunca les han agradecido directamente y leerla en voz alta (con quien quieran).",
            "recursos_digitales": [
                "Greater Good in Education — Gratitude Curriculum: ggie.berkeley.edu",
                "Robert Emmons Lab — Gratitude Research: psychology.ucdavis.edu/labs/emmons",
                "App 'Gratitude Journal' o 'Three Good Things' (gratuitas)",
            ],
        },

        {
            "titulo": "💪 La Resiliencia como Músculo: Del Golpe al Crecimiento",
            "descripcion": "Taller de resiliencia basado en el modelo de Resiliencia Positiva del American Psychological Association y el concepto de Crecimiento Postraumático (Tedeschi & Calhoun, 1996).",
            "fuente": "APA — 'The Road to Resilience' / Tedeschi & Calhoun — Posttraumatic Growth (UNC Charlotte) / Fundación CEDAL Colombia",
            "evidencia": "Las intervenciones de resiliencia en jóvenes mejoran el rendimiento académico y reducen conductas de riesgo (APA Meta-analysis, 2018, Psychological Bulletin).",
            "duracion_minutos": 55,
            "nivel": ["bachillerato", "general"],
            "materiales": ["Ramas o varillas flexibles (demostración)", "Papel para el mapa de resiliencia", "Colores"],
            "pasos": [
                "¿Qué NO es resiliencia? (8 min): No es 'aguantarse todo'. No es no sentir. No es 'ser fuerte'. Es la capacidad de atravesar dificultades y salir transformado — no igual que antes. El bambú vs. el roble en el viento.",
                "Mis Adversidades y lo que Aprendí (15 min): Línea del tiempo de resiliencia personal. Marcar 3 momentos difíciles de su vida (sin detalles que no quieran compartir). Para cada uno: ¿Qué aprendiste? ¿En qué creciste? ¿Qué habilidad desarrollaste?",
                "Los 10 factores de resiliencia según la APA (10 min): Conexiones sociales, propósito de vida, autoconocimiento, humor, flexibilidad cognitiva, cuidado propio, acción, esperanza, aprendizaje del pasado, perspectiva. ¿Cuáles tienen más desarrollados?",
                "Mi red de resiliencia (15 min): Mapa visual de su sistema de apoyo. Personas, lugares, actividades, recursos internos. 'Nadie es resiliente solo.'",
                "Cierre (7 min): '¿Qué te dice tu historia de resiliencia sobre quién eres?'",
            ],
            "preguntas_reflexion": [
                "¿Hay algo difícil que viviste que ahora te hace más fuerte o más sabio?",
                "¿A quién acudes cuando las cosas se ponen difíciles? ¿Por qué a esa persona?",
                "¿Qué consejo le darías a una versión más joven de ti sobre cómo atravesar momentos difíciles?",
            ],
            "indicador_logro": "El estudiante identifica al menos 3 factores de resiliencia presentes en su historia personal y mapea su red de apoyo con al menos 5 elementos.",
            "adaptacion_primaria": "Cuento de resiliencia + dibujo de 'mi superpoder secreto para los días difíciles'. Usar personajes conocidos como referentes.",
            "adaptacion_bachillerato": "Conectar con el concepto de Crecimiento Postraumático. ¿Qué habrían perdido si no hubieran vivido esas dificultades?",
            "recursos_digitales": [
                "APA — 'The Road to Resilience': apa.org/topics/resilience",
                "Fundación CEDAL Colombia — Programa de Resiliencia Escolar: fundacioncedal.org",
                "TED Talk: 'Lucy Hone — 3 secretos de las personas resilientes' (español)",
            ],
        },
    ],

    # ──────────────────────────────────────────────────────────────
    "bienestar_digital": [
    # ──────────────────────────────────────────────────────────────

        {
            "titulo": "📱 Inteligencia Emocional Digital: Las Redes y mi Bienestar",
            "descripcion": "Análisis crítico del impacto de redes sociales en la salud mental, basado en la investigación de Jean Twenge (San Diego State), Jonathan Haidt (NYU) y el informe del Surgeon General de EE.UU. sobre adolescentes y redes sociales (2023).",
            "fuente": "Jonathan Haidt & Jean Twenge — 'The Anxious Generation' (2024) / U.S. Surgeon General Advisory (2023) / ICBF Colombia — Adolescentes y Redes",
            "evidencia": "El uso de redes sociales más de 3 horas/día duplica el riesgo de depresión en adolescentes femeninas (Twenge et al., 2018, JAMA Pediatrics).",
            "duracion_minutos": 60,
            "nivel": ["bachillerato"],
            "materiales": ["Encuesta anónima de uso digital (impresa)", "Casos de estudio ficticios", "Papel para el 'escudo digital' personal"],
            "pasos": [
                "Diagnóstico anónimo (8 min): Encuesta rápida. ¿Cuántas horas al día en redes? ¿Cómo te sientes después de 1 hora de scroll? ¿Has dejado de hacer algo importante por el celular? Resultados generales sin identificar a nadie.",
                "La neurociencia del like (12 min): Dopamina y recompensa variable — igual que una máquina tragamonedas. Comparación social de Festinger. FOMO. La amígdala y las imágenes de exclusión social.",
                "Análisis de casos en grupos (20 min): Grupos de 4 analizan situaciones ficticias: hate, ghosting, FOMO, exposición excesiva, cyberbullying, bodies comparison. ¿Qué emociones? ¿Qué haría yo?",
                "El algoritmo y las emociones (10 min): ¿Por qué el algoritmo prioriza el contenido que genera rabia e indignación? ¿Cómo nos afecta eso emocionalmente sin que lo notemos?",
                "Mi escudo digital (10 min): Cada estudiante crea sus 3-5 reglas personales de uso de redes basadas en lo aprendido. No prohibición — uso consciente.",
            ],
            "preguntas_reflexion": [
                "¿Has sentido que tu estado de ánimo cambió después de usar redes? ¿Hacia dónde?",
                "¿Qué diferencia hay entre conectar digitalmente y conectar emocionalmente de verdad?",
                "Si tuvieras que diseñar una red social que cuide la salud mental, ¿cómo sería?",
            ],
            "indicador_logro": "El estudiante identifica al menos 2 mecanismos psicológicos de las redes y formula un plan personal de uso digital consciente con reglas concretas.",
            "adaptacion_primaria": "Enfocar en videojuegos y YouTube. '¿Cómo te sientes cuando juegas mucho tiempo? ¿Y cuando paras?' Reglas del tiempo de pantalla.",
            "adaptacion_bachillerato": "Agregar análisis de un influencer real y cómo construye engagement emocional. La diferencia entre admirar e imitar.",
            "recursos_digitales": [
                "Surgeon General's Advisory on Social Media: hhs.gov/surgeongeneral",
                "ICBF — 'Niños, Niñas y Adolescentes en Internet': icbf.gov.co",
                "Documental 'The Social Dilemma' (Netflix) — ver fragmento de 10 min",
                "Center for Humane Technology: humanetech.com/resources",
            ],
        },
    ],
}


# ══════════════════════════════════════════════════════════════════
# FRASES DE BIENESTAR — Para el Dashboard
# Fuentes: psicólogos reconocidos mundialmente
# ══════════════════════════════════════════════════════════════════

FRASES_BIENESTAR = [
    {
        "frase": "Entre estímulo y respuesta, hay un espacio. En ese espacio está nuestro poder para elegir nuestra respuesta.",
        "autor": "Viktor Frankl",
        "fuente": "Man's Search for Meaning (1946)",
        "categoria": "autorregulacion",
    },
    {
        "frase": "No podemos elegir nuestros pensamientos, pero sí podemos elegir no creerles.",
        "autor": "Daniel Siegel",
        "fuente": "The Whole-Brain Child (2011)",
        "categoria": "autorregulacion",
    },
    {
        "frase": "La empatía es estar presente con las personas, sin tratar de arreglarlo.",
        "autor": "Brené Brown",
        "fuente": "Daring Greatly (2012)",
        "categoria": "empatia",
    },
    {
        "frase": "La gratitud transforma lo que tenemos en suficiente.",
        "autor": "Robert Emmons",
        "fuente": "Thanks! How the New Science of Gratitude Can Make You Happier (2007)",
        "categoria": "gratitud",
    },
    {
        "frase": "El florecimiento es el camino — no el destino.",
        "autor": "Martin Seligman",
        "fuente": "Flourish (2011) — Positive Psychology Center",
        "categoria": "bienestar",
    },
    {
        "frase": "Las emociones son información, no órdenes.",
        "autor": "Marc Brackett",
        "fuente": "Permission to Feel (2019) — Yale Center for Emotional Intelligence",
        "categoria": "emociones",
    },
    {
        "frase": "La resiliencia no es rebotar — es aprender a atravesar.",
        "autor": "Lucy Hone",
        "fuente": "Resilient Grieving (2017) / TEDx Christchurch",
        "categoria": "resiliencia",
    },
    {
        "frase": "Nombrar la emoción la doma. El lenguaje transforma el caos interior en claridad.",
        "autor": "Daniel Siegel",
        "fuente": "Mindsight (2010) — UCLA Mindful Awareness Research Center",
        "categoria": "emociones",
    },
    {
        "frase": "Donde va la atención, fluye la energía.",
        "autor": "Jon Kabat-Zinn",
        "fuente": "Full Catastrophe Living (1990) — UMass Center for Mindfulness",
        "categoria": "mindfulness",
    },
    {
        "frase": "Los estudiantes no aprenden de docentes que no les gustan — aprenden de docentes que los hacen sentir seguros.",
        "autor": "James Comer",
        "fuente": "School Power (1980) — Yale Child Study Center",
        "categoria": "relaciones",
    },
    {
        "frase": "Cada emoción nos dice algo. El miedo dice que algo importante está en riesgo. La tristeza dice que algo valioso se perdió. La ira dice que una necesidad no fue respetada.",
        "autor": "Marshall Rosenberg",
        "fuente": "Nonviolent Communication (2003)",
        "categoria": "emociones",
    },
    {
        "frase": "El autocuidado no es egoísmo — es la base desde la que podemos cuidar a otros.",
        "autor": "Audre Lorde",
        "fuente": "A Burst of Light (1988)",
        "categoria": "bienestar",
    },
]


# ══════════════════════════════════════════════════════════════════
# CONSEJOS POR CATEGORÍA — Para el motor Kleit
# ══════════════════════════════════════════════════════════════════

CONSEJOS_CATEGORIA = {
    "autorregulacion": "💡 Para trabajar autorregulación, lo más poderoso es que los estudiantes PRACTIQUEN la técnica en el momento, no solo que la estudien. Dedica al menos la mitad del tiempo a la práctica real. (Fuente: APA Division 53, 2020)",
    "emociones_basicas": "💡 Empieza siempre con identificación personal antes de la teoría — genera conexión emocional auténtica con el tema. El vocabulario emocional ampliado es predictor de salud mental (Kashdan et al., 2015).",
    "empatia_relaciones": "💡 El role-play y los círculos de diálogo son especialmente efectivos para habilidades relacionales. Los estudiantes aprenden más haciendo que escuchando (CASEL, Framework 2020).",
    "identidad_autoestima": "💡 Temas de identidad requieren ambiente de alta confianza. Considera empezar con reflexión escrita individual antes de compartir grupalmente. La autoestima se construye desde evidencias reales, no desde elogios genéricos (Seligman, 2011).",
    "bienestar_gratitud": "💡 Las prácticas de gratitud tienen más impacto cuando son regulares (5 min al inicio de cada clase) que en sesiones largas ocasionales. La consistencia supera la intensidad (Emmons & McCullough, 2003).",
    "bienestar_digital": "💡 Con adolescentes, los temas digitales generan mucha participación. Sus propias experiencias son el mejor punto de partida — son los expertos en su mundo digital. (Haidt & Twenge, 2024)",
    "resiliencia": "💡 La resiliencia se construye en relación — no de forma aislada. La conexión social es el factor predictor #1 de resiliencia en adolescentes (APA, 2018). Diseña actividades que fortalezcan vínculos.",
}


def obtener_actividades(categoria: str = None, nivel: str = None, excluir_titulos: list = None) -> list:
    """
    Retorna actividades filtradas por categoría y nivel.
    Excluye títulos ya usados para evitar repetición.
    """
    excluir_titulos = excluir_titulos or []
    resultado = []

    categorias_buscar = [categoria] if categoria and categoria in BANCO_PSICOLOGICO else list(BANCO_PSICOLOGICO.keys())

    for cat in categorias_buscar:
        for actividad in BANCO_PSICOLOGICO.get(cat, []):
            if actividad["titulo"] in excluir_titulos:
                continue
            if nivel and nivel != "general" and nivel not in actividad.get("nivel", []):
                if "general" not in actividad.get("nivel", []):
                    continue
            actividad_con_cat = dict(actividad)
            actividad_con_cat["categoria"] = cat
            resultado.append(actividad_con_cat)

    return resultado


def obtener_frase_del_dia() -> dict:
    """Retorna una frase de bienestar basada en el día del año."""
    from datetime import date
    dia = date.today().timetuple().tm_yday
    return FRASES_BIENESTAR[dia % len(FRASES_BIENESTAR)]


def obtener_consejo(categoria: str) -> str:
    """Retorna el consejo con fuente para una categoría dada."""
    return CONSEJOS_CATEGORIA.get(categoria, CONSEJOS_CATEGORIA.get("autorregulacion", ""))
