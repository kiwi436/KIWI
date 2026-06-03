"""
Modelos de KIWI v4.

Cada modelo de datos (Clase, Tarea, Recurso, IdeaKleit, SesionKleit, PlanDeAula)
tiene FK a Usuario para aislar los datos por usuario.
"""

from django.db import models
from django.utils import timezone


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    # Contraseña almacenada con lógica propia — no usa django.contrib.auth.hashers.make_password
    password_hash = models.CharField(max_length=200)
    recibir_correos = models.BooleanField(default=False)
    email_verificado = models.BooleanField(default=True)
    token_verificacion = models.CharField(max_length=100, blank=True)
    google_refresh_token = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Clase(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    grupo = models.CharField(max_length=100)
    tema = models.TextField(blank=True)
    fecha = models.DateTimeField()
    recordatorio = models.BooleanField(default=True)
    completada = models.BooleanField(default=False)
    # Satisfacción de la clase: entero 1–6 correspondiente a los 6 emojis (😢→😄)
    satisfaccion = models.IntegerField(null=True, blank=True)
    notas = models.TextField(blank=True)
    google_event_id = models.CharField(max_length=200, blank=True)
    # Recurrencia
    es_recurrente = models.BooleanField(default=False)
    frecuencia_semanas = models.IntegerField(null=True, blank=True)  # 1=semanal, 2=quincenal
    fecha_fin_recurrencia = models.DateField(null=True, blank=True)
    clase_padre = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='recurrencias'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f"{self.titulo} - {self.grupo}"

    @property
    def es_hoy(self):
        return self.fecha.date() == timezone.now().date()

    @property
    def es_pasada(self):
        return self.fecha < timezone.now()


class Tarea(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)
    ESTADO_CHOICES = [
        ('no_empezada', 'No empezada'),
        ('en_proceso', 'En proceso'),
        ('completada', 'Completada'),
    ]
    titulo = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='no_empezada')
    plazo = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['plazo']

    def __str__(self):
        return self.titulo


class Recurso(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)
    CICLO_CHOICES = [
        ('ciclo_inicial', 'Ciclo Inicial (Jardín y Transición)'),
        ('ciclo_uno', 'Ciclo 1 (1° y 2° Primaria)'),
        ('ciclo_dos', 'Ciclo 2 (3° a 5° Primaria)'),
        ('ciclo_tres', 'Ciclo 3 (6° a 8° Bachillerato)'),
        ('ciclo_cuatro', 'Ciclo 4 (9° a 11° Bachillerato)'),
    ]
    TIPO_CHOICES = [
        ('documento', 'Documento'),
        ('video', 'Video'),
        ('enlace', 'Enlace web'),
        ('planilla', 'Planilla'),
        ('actividad', 'Actividad'),
        ('otro', 'Otro'),
    ]
    titulo = models.CharField(max_length=200)
    ciclo = models.CharField(max_length=20, choices=CICLO_CHOICES, default='ciclo_uno')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='otro')
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='recursos/', blank=True, null=True)
    enlace = models.URLField(blank=True)
    etiquetas = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def creado_en(self):
        return self.created_at

    def __str__(self):
        return self.titulo


class IdeaKleit(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tema_original = models.CharField(max_length=200)
    grupo_original = models.CharField(max_length=100)
    # Texto enriquecido generado por _formatear_expansion() en views.py (pasos, materiales, etc.)
    expansion = models.TextField(blank=True)
    guardada = models.BooleanField(default=False)
    usada_en_clase = models.ForeignKey(Clase, null=True, blank=True, on_delete=models.SET_NULL, related_name='ideas_kleit')
    recursos_sugeridos = models.TextField(blank=True)
    actividades_detalle = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.titulo


class SesionKleit(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)
    titulo_sesion = models.CharField(max_length=200, blank=True)
    tema = models.CharField(max_length=200, blank=True)
    grupo = models.CharField(max_length=100, blank=True)
    nivel_detectado = models.CharField(max_length=50, blank=True)
    # JSON array: [{role, content, grupo?, ts, fuente?}]
    mensajes = models.TextField(blank=True, default='[]')
    ideas = models.ManyToManyField(IdeaKleit, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    @property
    def creada_en(self):
        return self.created_at

    def __str__(self):
        return f"Kleit: {self.tema} ({self.grupo})"


class PlanDeAula(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)
    GRADO_CHOICES = [
        ('jardin', 'Jardín'),
        ('transicion', 'Transición'),
        ('primero', '1° Primaria'),
        ('segundo', '2° Primaria'),
        ('tercero', '3° Primaria'),
        ('cuarto', '4° Primaria'),
        ('quinto', '5° Primaria'),
        ('sexto', '6° Bachillerato'),
        ('septimo', '7° Bachillerato'),
        ('octavo', '8° Bachillerato'),
        ('noveno', '9° Bachillerato'),
        ('decimo', '10° Bachillerato'),
        ('once', '11° Bachillerato'),
    ]
    PERIODO_CHOICES = [
        ('I', 'Período I'),
        ('II', 'Período II'),
        ('III', 'Período III'),
        ('IV', 'Período IV'),
    ]
    COMPETENCIA_SEL_CHOICES = [
        ('autoconciencia', 'Autoconciencia — Reconocimiento emocional'),
        ('autogestion', 'Autogestión — Regulación emocional'),
        ('conciencia_social', 'Conciencia Social — Empatía y perspectiva'),
        ('habilidades_relacionales', 'Habilidades Relacionales — Comunicación y vínculos'),
        ('toma_decisiones', 'Toma de Decisiones Responsable'),
        ('bienestar_integral', 'Bienestar Integral — Enfoque holístico'),
    ]
    METODOLOGIA_CHOICES = [
        ('integrado', 'Enfoque Integrado (Multi-metodológico)'),
    ]
    TIPO_CHOICES = [
        ('plan_aula', 'Plan de Aula'),
        ('pensum', 'Pensum / Malla Curricular'),
    ]
    CICLO_MAP = {
        'jardin': 'Ciclo Inicial',
        'transicion': 'Ciclo Inicial',
        'primero': 'Ciclo I',
        'segundo': 'Ciclo I',
        'tercero': 'Ciclo II',
        'cuarto': 'Ciclo II',
        'quinto': 'Ciclo II',
        'sexto': 'Ciclo III',
        'septimo': 'Ciclo III',
        'octavo': 'Ciclo III',
        'noveno': 'Ciclo IV',
        'decimo': 'Ciclo IV',
        'once': 'Ciclo IV',
    }
    # ── Identificación ──────────────────────────────
    tipo          = models.CharField(max_length=20, choices=TIPO_CHOICES, default='plan_aula')
    titulo        = models.CharField(max_length=200)
    grado         = models.CharField(max_length=20, choices=GRADO_CHOICES)
    periodo       = models.CharField(max_length=5, choices=PERIODO_CHOICES, default='I', blank=True)
    metodologia   = models.CharField(max_length=30, choices=METODOLOGIA_CHOICES, default='integrado')
    # ── Competencia SEL (¿Qué se trabaja?) ──────────
    competencias  = models.CharField(max_length=50, choices=COMPETENCIA_SEL_CHOICES,
                                     default='bienestar_integral', blank=True)
    # ── Desempeño (¿Qué logrará el estudiante?) ─────
    objetivo_general   = models.TextField()          # → DESEMPEÑO
    # ── Temas (¿Cuáles son los temas?) ──────────────
    contenido_tematico = models.TextField(blank=True) # → TEMAS PARA TRABAJAR
    # ── Estrategia (¿Cómo?) ─────────────────────────
    estrategias        = models.TextField(blank=True) # → ESTRATEGIA DE APRENDIZAJE
    # ── Valoración continua ──────────────────────────
    evaluacion         = models.TextField(blank=True) # → VALORACIÓN CONTINUA
    # ── Recursos ────────────────────────────────────
    recursos_didacticos = models.TextField(blank=True)
    # ── Planificación temporal ──────────────────────
    duracion_semanas   = models.IntegerField(default=4)
    # ── Contenido generado por IA (JSON) ────────────
    contenido_ia       = models.TextField(blank=True)
    # ── Lista de desempeños con su contenido IA (JSON array) ────
    desempenios_json   = models.TextField(blank=True, default='[]')
    created_at         = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def ciclo(self):
        return self.CICLO_MAP.get(self.grado, 'General')

    @property
    def competencia_display(self):
        return dict(self.COMPETENCIA_SEL_CHOICES).get(self.competencias, self.competencias)

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.titulo} ({self.get_grado_display()})"


class ConfiguracionApp(models.Model):
    """Configuración global de la app — solo debe existir un registro."""
    gmail_refresh_token = models.CharField(max_length=500, blank=True)
    gmail_email = models.EmailField(blank=True)

    class Meta:
        verbose_name = 'Configuración'

    def __str__(self):
        return f"Configuración — Gmail: {self.gmail_email or 'no conectado'}"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
