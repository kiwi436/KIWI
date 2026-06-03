from django.urls import path
from . import views

urlpatterns = [
    # ── Auth ─────────────────────────────────────────────────────
    path('', views.landing, name='landing'),
    path('sobre-kiwi/', views.sobre_kiwi, name='sobre_kiwi'),
    path('sobre-kleit/', views.sobre_kleit, name='sobre_kleit'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('verificar-email/', views.verificar_email_view, name='verificar_email'),
    path('reenviar-verificacion/', views.reenviar_verificacion_view, name='reenviar_verificacion'),
    path('recuperar-password/', views.recuperar_password_view, name='recuperar_password'),
    path('recuperar-password/confirmar/', views.recuperar_password_confirmar_view, name='recuperar_password_confirmar'),
    path('configuracion/gmail/conectar/', views.gmail_conectar_view, name='gmail_conectar'),
    path('configuracion/gmail/callback/', views.gmail_callback_view, name='gmail_callback'),
    path('perfil/', views.perfil_view, name='perfil'),

    # ── App ──────────────────────────────────────────────────────
    path('dashboard/', views.dashboard, name='dashboard'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('calendario/completar/<int:pk>/', views.completar_clase, name='completar_clase'),
    path('calendario/eliminar/<int:pk>/', views.eliminar_clase, name='eliminar_clase'),
    path('calendario/satisfaccion/<int:pk>/', views.satisfaccion_clase, name='satisfaccion_clase'),

    # ── Google Calendar ──────────────────────────────────────────
    path('calendario/google/conectar/', views.google_auth_start, name='google_auth_start'),
    path('calendario/google/callback/', views.google_auth_callback, name='google_auth_callback'),
    path('google/callback/', views.google_auth_callback, name='google_callback_short'),
    path('calendario/google/desconectar/', views.google_disconnect, name='google_disconnect'),
    path('calendario/google/sync/<int:pk>/', views.google_sync_clase, name='google_sync_clase'),
    path('calendario/google/sync-todas/', views.google_sync_todas, name='google_sync_todas'),

    # ── Plan de Aula ─────────────────────────────────────────────
    path('plan-aula/', views.plan_aula_view, name='plan_aula'),
    path('plan-aula/generar/', views.plan_aula_generar, name='plan_aula_generar'),
    path('plan-aula/<int:pk>/', views.plan_aula_detalle, name='plan_aula_detalle'),
    path('plan-aula/eliminar/<int:pk>/', views.eliminar_plan_aula, name='eliminar_plan_aula'),
    path('plan-aula/exportar/<int:pk>/', views.exportar_plan_pdf, name='exportar_plan_pdf'),
    path('plan-aula/descargar/<int:pk>/', views.descargar_plan_pdf, name='descargar_plan_pdf'),

    # ── Kleit ────────────────────────────────────────────────────
    path('kleit/', views.kleit_view, name='kleit'),
    path('kleit/chat/', views.kleit_chat_ajax, name='kleit_chat'),
    path('kleit/eliminar/<int:pk>/', views.kleit_eliminar_sesion, name='kleit_eliminar_sesion'),
    path('kleit/guardar/<int:pk>/', views.guardar_idea, name='guardar_idea'),
    path('kleit/ideas-guardadas/', views.ideas_guardadas_view, name='ideas_guardadas'),
    path('kleit/asignar/<int:pk>/', views.asignar_idea_clase, name='asignar_idea'),
    path('kleit/exportar-clase/<int:pk>/', views.exportar_plan_clase_pdf, name='exportar_plan_clase'),

    # ── Recursos & Tareas ────────────────────────────────────────
    path('recursos/', views.recursos_view, name='recursos'),
    path('recursos/eliminar/<int:pk>/', views.eliminar_recurso, name='eliminar_recurso'),
    path('tareas/', views.tareas_view, name='tareas'),

    # ── APIs ─────────────────────────────────────────────────────
    path('api/clases/', views.api_clases_json, name='api_clases'),
    path('api/notificaciones/', views.api_clases_proximas, name='api_notificaciones'),
    path('api/kleit/estado/', views.api_estado_kleit, name='api_estado_kleit'),
    path('api/google/eventos/', views.api_google_eventos, name='api_google_eventos'),
    path('api/frase-dia/', views.api_frase_dia, name='api_frase_dia'),
]
