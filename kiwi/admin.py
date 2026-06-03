from django.contrib import admin
from .models import Clase, Tarea, Recurso, IdeaKleit, SesionKleit

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ['titulo','grupo','fecha','completada','satisfaccion']
    list_filter = ['completada','grupo']

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo','estado','plazo']
    list_filter = ['estado']

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ['titulo','tipo','created_at']

@admin.register(IdeaKleit)
class IdeaKleitAdmin(admin.ModelAdmin):
    list_display = ['titulo','guardada','tema_original','grupo_original']
    list_filter = ['guardada']

@admin.register(SesionKleit)
class SesionKleitAdmin(admin.ModelAdmin):
    list_display = ['tema','grupo','nivel_detectado','created_at']
