from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
import json
import threading
from datetime import timedelta, date

from hashlib import sha256

from .models import Clase, Tarea, Recurso, IdeaKleit, SesionKleit, PlanDeAula, Usuario
from .kleit_engine import chat_con_kleit, generar_ideas


def _ctx(request, extra=None):
    """Construye el contexto base con datos de sesión del usuario."""
    ctx = {
        'usuario_nombre': request.session.get('usuario_nombre', 'usuario'),
        'usuario_correo': request.session.get('usuario_correo', ''),
        'usuario_institucion': request.session.get('usuario_institucion', 'Colegio San Francisco de Asís'),
        'usuario_id': request.session.get('usuario_id'),
        'usuario_foto': request.session.get('usuario_foto', ''),
    }
    if extra:
        ctx.update(extra)
    return ctx


def _uid(request):
    """Retorna el ID del usuario logueado, o None si no hay sesión."""
    return request.session.get('usuario_id')


def _login_required(request):
    """Guarda de autenticación. Retorna True si hay sesión activa con usuario_id."""
    return bool(request.session.get('usuario_id'))


def landing(request):
    if _login_required(request):
        return redirect('dashboard')
    return render(request, 'kiwi/landing.html')


def sobre_kiwi(request):
    return render(request, 'kiwi/sobre_kiwi.html')


def sobre_kleit(request):
    return render(request, 'kiwi/sobre_kleit.html')


def login_view(request):
    """Login por correo y contraseña — verifica contra la BD y almacena usuario_id en sesión."""
    if _login_required(request):
        return redirect('dashboard')
    error = None
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        password = request.POST.get('password', '').strip()
        if not correo or not password:
            error = 'Por favor completa todos los campos.'
        else:
            try:
                usuario = Usuario.objects.get(correo=correo)
                if usuario.password_hash == sha256(password.encode()).hexdigest():
                    if not usuario.email_verificado:
                        return render(request, 'kiwi/login.html', {
                            'error': 'Debes verificar tu correo electrónico antes de iniciar sesión. Revisa tu bandeja de entrada.',
                            'correo_sin_verificar': correo,
                        })
                    request.session['usuario_id'] = usuario.pk
                    request.session['usuario_nombre'] = usuario.nombre
                    request.session['usuario_correo'] = usuario.correo
                    request.session['usuario_institucion'] = getattr(usuario, 'institucion', 'Colegio San Francisco de Asís')
                    if usuario.google_refresh_token:
                        request.session['google_refresh_token'] = usuario.google_refresh_token
                        request.session['google_connected'] = True
                    request.session.modified = True
                    return redirect('dashboard')
                else:
                    error = 'Contraseña incorrecta.'
            except Usuario.DoesNotExist:
                error = 'No existe una cuenta con ese correo.'
    return render(request, 'kiwi/login.html', {'error': error})


def registro_view(request):
    """Registro en dos pasos. Paso 2 crea el registro Usuario en BD y almacena usuario_id en sesión."""
    if _login_required(request):
        return redirect('dashboard')
    error = None
    if request.method == 'POST':
        step = request.POST.get('step', '1')
        if step == '1':
            nombres = request.POST.get('nombres', '').strip()
            apellidos = request.POST.get('apellidos', '').strip()
            if not nombres:
                error = 'El nombre es obligatorio.'
                return render(request, 'kiwi/registro.html', {'step': 1, 'error': error})
            request.session['reg_nombre'] = nombres
            request.session['reg_apellidos'] = apellidos
            request.session['reg_telefono'] = request.POST.get('telefono', '')
            request.session['reg_direccion'] = request.POST.get('direccion', '')
            request.session.modified = True
            return render(request, 'kiwi/registro.html', {'step': 2, 'nombre': nombres})
        else:
            correo = request.POST.get('correo', '').strip()
            password = request.POST.get('password', '').strip()
            confirm = request.POST.get('confirm_password', '').strip()
            acepto = request.POST.get('acepto_terminos')
            if not correo or not password:
                error = 'El correo y la contraseña son obligatorios.'
            elif password != confirm:
                error = 'Las contraseñas no coinciden.'
            elif len(password) < 8:
                error = 'La contraseña debe tener mínimo 8 caracteres.'
            elif not acepto:
                error = 'Debes aceptar los términos y condiciones.'
            elif Usuario.objects.filter(correo=correo).exists():
                error = 'Ya existe una cuenta con ese correo.'
            else:
                import random
                from django.core.mail import send_mail
                nombre = request.session.get('reg_nombre', correo.split('@')[0])
                codigo = str(random.randint(100000, 999999))
                usuario = Usuario.objects.create(
                    nombre=nombre,
                    apellidos=request.session.get('reg_apellidos', ''),
                    correo=correo,
                    telefono=request.session.get('reg_telefono', ''),
                    direccion=request.session.get('reg_direccion', ''),
                    password_hash=sha256(password.encode()).hexdigest(),
                    email_verificado=False,
                    token_verificacion=codigo,
                )
                email_enviado = False
                try:
                    send_mail(
                        subject='Tu código de verificación KIWI',
                        message=(
                            f'Hola {nombre},\n\n'
                            f'Tu código de verificación es:\n\n'
                            f'        {codigo}\n\n'
                            f'Ingrésalo en la aplicación para activar tu cuenta.\n'
                            f'El código expira cuando solicites uno nuevo.\n\n'
                            f'Si no creaste esta cuenta puedes ignorar este mensaje.\n\n'
                            f'— El equipo de KIWI'
                        ),
                        from_email=None,
                        recipient_list=[correo],
                        fail_silently=False,
                    )
                    email_enviado = True
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).error(f'Error enviando correo de verificación a {correo}: {e}')
                return render(request, 'kiwi/registro.html', {
                    'verificacion_enviada': True,
                    'correo': correo,
                    'email_enviado': email_enviado,
                    'codigo_fallback': codigo if not email_enviado else None,
                })
            return render(request, 'kiwi/registro.html', {
                'step': 2, 'error': error,
                'nombre': request.session.get('reg_nombre', ''),
            })
    return render(request, 'kiwi/registro.html', {'step': 1})


def logout_view(request):
    request.session.flush()
    return redirect('landing')


def verificar_email_view(request):
    """Valida el código de 6 dígitos enviado al correo del usuario."""
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        codigo = request.POST.get('codigo', '').strip()
        try:
            usuario = Usuario.objects.get(correo=correo, token_verificacion=codigo, email_verificado=False)
            usuario.email_verificado = True
            usuario.token_verificacion = ''
            usuario.save()
            messages.success(request, f'¡Correo verificado! Ya puedes iniciar sesión, {usuario.nombre}.')
            return redirect('login')
        except Usuario.DoesNotExist:
            return render(request, 'kiwi/verificar_email.html', {
                'correo': correo,
                'error': 'Código incorrecto. Verifica que lo hayas escrito bien o solicita uno nuevo.',
            })
    correo = request.GET.get('correo', '')
    return render(request, 'kiwi/verificar_email.html', {'correo': correo})


def reenviar_verificacion_view(request):
    if request.method == 'POST':
        import random
        from django.core.mail import send_mail
        correo = request.POST.get('correo', '').strip()
        try:
            usuario = Usuario.objects.get(correo=correo, email_verificado=False)
            codigo = str(random.randint(100000, 999999))
            usuario.token_verificacion = codigo
            usuario.save()
            try:
                send_mail(
                    subject='Tu código de verificación KIWI',
                    message=(
                        f'Hola {usuario.nombre},\n\n'
                        f'Tu nuevo código de verificación es:\n\n'
                        f'        {codigo}\n\n'
                        f'Ingrésalo en la aplicación para activar tu cuenta.\n\n'
                        f'— El equipo de KIWI'
                    ),
                    from_email=None,
                    recipient_list=[correo],
                    fail_silently=False,
                )
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f'Error reenviando código a {correo}: {e}')
        except Usuario.DoesNotExist:
            pass
    correo = request.POST.get('correo', '').strip()
    return redirect(f'/verificar-email/?correo={correo}')


def recuperar_password_view(request):
    """Paso 1: el usuario ingresa su correo y recibe un código de 6 dígitos."""
    if request.method == 'POST':
        import random
        from django.core.mail import send_mail
        correo = request.POST.get('correo', '').strip().lower()
        try:
            usuario = Usuario.objects.get(correo=correo)
            codigo = str(random.randint(100000, 999999))
            usuario.token_verificacion = codigo
            usuario.save()
            email_enviado = False
            try:
                send_mail(
                    subject='Recupera tu contraseña KIWI',
                    message=(
                        f'Hola {usuario.nombre},\n\n'
                        f'Tu código para restablecer la contraseña es:\n\n'
                        f'        {codigo}\n\n'
                        f'Ingrésalo en la aplicación para crear una nueva contraseña.\n'
                        f'Si no solicitaste esto, ignora este mensaje.\n\n'
                        f'— El equipo de KIWI'
                    ),
                    from_email=None,
                    recipient_list=[correo],
                    fail_silently=False,
                )
                email_enviado = True
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f'Error enviando correo recuperación a {correo}: {e}')
            return render(request, 'kiwi/recuperar_password.html', {
                'paso': 2,
                'correo': correo,
                'email_enviado': email_enviado,
                'codigo_fallback': codigo if not email_enviado else None,
            })
        except Usuario.DoesNotExist:
            return render(request, 'kiwi/recuperar_password.html', {
                'paso': 1,
                'error': 'No existe ninguna cuenta con ese correo.',
            })
    return render(request, 'kiwi/recuperar_password.html', {'paso': 1})


def recuperar_password_confirmar_view(request):
    """Paso 2 y 3: verifica el código y establece la nueva contraseña."""
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip().lower()
        codigo = request.POST.get('codigo', '').strip()
        nueva = request.POST.get('nueva_password', '')
        confirmar = request.POST.get('confirmar_password', '')
        try:
            usuario = Usuario.objects.get(correo=correo, token_verificacion=codigo)
        except Usuario.DoesNotExist:
            return render(request, 'kiwi/recuperar_password.html', {
                'paso': 2,
                'correo': correo,
                'error': 'Código incorrecto. Verifica que lo hayas escrito bien.',
                'email_enviado': True,
            })
        if len(nueva) < 8:
            return render(request, 'kiwi/recuperar_password.html', {
                'paso': 3,
                'correo': correo,
                'codigo': codigo,
                'error': 'La contraseña debe tener al menos 8 caracteres.',
            })
        if nueva != confirmar:
            return render(request, 'kiwi/recuperar_password.html', {
                'paso': 3,
                'correo': correo,
                'codigo': codigo,
                'error': 'Las contraseñas no coinciden.',
            })
        usuario.password_hash = sha256(nueva.encode()).hexdigest()
        usuario.token_verificacion = ''
        usuario.save()
        messages.success(request, '¡Contraseña actualizada! Ya puedes iniciar sesión.')
        return redirect('login')
    # GET con código ya verificado → mostrar formulario de nueva contraseña
    correo = request.GET.get('correo', '')
    codigo = request.GET.get('codigo', '')
    if correo and codigo:
        try:
            Usuario.objects.get(correo=correo, token_verificacion=codigo)
            return render(request, 'kiwi/recuperar_password.html', {
                'paso': 3, 'correo': correo, 'codigo': codigo,
            })
        except Usuario.DoesNotExist:
            pass
    return redirect('recuperar_password')


def dashboard(request):
    if not _login_required(request):
        return redirect('login')
    hoy = timezone.now()
    uid = _uid(request)
    return render(request, 'kiwi/dashboard.html', {
        'clases_hoy': Clase.objects.filter(usuario_id=uid, fecha__date=hoy.date(), completada=False).order_by('fecha'),
        'proximas': Clase.objects.filter(usuario_id=uid, fecha__gte=hoy, completada=False).order_by('fecha')[:5],
        'tareas': Tarea.objects.filter(usuario_id=uid)[:5],
        'ideas_guardadas': IdeaKleit.objects.filter(usuario_id=uid, guardada=True)[:4],
        'planes_recientes': PlanDeAula.objects.filter(usuario_id=uid)[:3],
        'hora': hoy,
        'usuario_nombre': request.session.get('usuario_nombre', 'usuario'),
        'usuario_correo': request.session.get('usuario_correo', ''),
        'usuario_institucion': request.session.get('usuario_institucion', ''),
    })


def calendario_view(request):
    if not _login_required(request):
        return redirect('login')
    hoy = timezone.now()
    if request.method == 'POST':
        from django.utils.dateparse import parse_datetime
        titulo = request.POST.get('titulo', '').strip()
        grupo = request.POST.get('grupo', '').strip()
        fecha_str = request.POST.get('fecha', '')
        es_recurrente = request.POST.get('es_recurrente') == 'on'
        frecuencia = request.POST.get('frecuencia_semanas', '1')
        duracion_meses = request.POST.get('duracion_meses', '0')

        uid = _uid(request)
        if titulo and grupo and fecha_str:
            fd = parse_datetime(fecha_str)
            if fd:
                if timezone.is_naive(fd):
                    fd = timezone.make_aware(fd)
                clase_padre = Clase.objects.create(
                    usuario_id=uid,
                    titulo=titulo, grupo=grupo,
                    tema=request.POST.get('tema', ''),
                    fecha=fd, notas=request.POST.get('notas', ''),
                    recordatorio=request.POST.get('recordatorio') == 'on',
                    es_recurrente=es_recurrente,
                    frecuencia_semanas=int(frecuencia) if es_recurrente else None,
                )

                # Crear clases recurrentes
                if es_recurrente:
                    meses = int(duracion_meses) if duracion_meses else 10
                    freq_semanas = int(frecuencia) if frecuencia else 1
                    fecha_actual = fd
                    fecha_limite = fd + timedelta(days=meses * 30)
                    clase_padre.fecha_fin_recurrencia = fecha_limite.date()
                    clase_padre.save()

                    while True:
                        fecha_actual = fecha_actual + timedelta(weeks=freq_semanas)
                        if fecha_actual.date() > fecha_limite.date():
                            break
                        Clase.objects.create(
                            usuario_id=uid,
                            titulo=titulo, grupo=grupo,
                            tema=request.POST.get('tema', ''),
                            fecha=fecha_actual,
                            notas=request.POST.get('notas', ''),
                            recordatorio=request.POST.get('recordatorio') == 'on',
                            es_recurrente=True,
                            frecuencia_semanas=freq_semanas,
                            clase_padre=clase_padre,
                        )
                    total = Clase.objects.filter(clase_padre=clase_padre).count()
                    messages.success(request, f'Clase "{titulo}" programada {total + 1} veces durante {meses} meses.')
                else:
                    messages.success(request, f'Clase "{titulo}" agregada al calendario.')
        return redirect('calendario')

    uid = _uid(request)
    from . import google_calendar as gcal_mod
    return render(request, 'kiwi/calendario.html', {
        'clases': Clase.objects.filter(usuario_id=uid).order_by('fecha'),
        'clases_hoy': Clase.objects.filter(usuario_id=uid, fecha__date=hoy.date()).order_by('fecha'),
        'proximas': Clase.objects.filter(usuario_id=uid, fecha__gte=hoy, completada=False).order_by('fecha')[:5],
        'hoy': hoy,
        'google_conectado': gcal_mod.is_connected(request.session),
        'usuario_nombre': request.session.get('usuario_nombre', 'usuario'),
        'usuario_correo': request.session.get('usuario_correo', ''),
        'usuario_institucion': request.session.get('usuario_institucion', ''),
    })


def completar_clase(request, pk):
    c = get_object_or_404(Clase, pk=pk, usuario_id=_uid(request))
    c.completada = not c.completada
    c.save()
    messages.success(request, f'Clase marcada como {"completada" if c.completada else "pendiente"}.')
    return redirect('calendario')


def eliminar_clase(request, pk):
    c = get_object_or_404(Clase, pk=pk, usuario_id=_uid(request))
    nombre = c.titulo
    if c.google_event_id:
        from . import google_calendar as gcal
        gcal.eliminar_evento_google(request.session, c.google_event_id)
    c.delete()
    messages.success(request, f'Clase "{nombre}" eliminada.')
    return redirect('calendario')


def satisfaccion_clase(request, pk):
    """Endpoint AJAX — recibe JSON {satisfaccion: 1-6} y guarda en Clase.satisfaccion.
    Llamado desde el modal de detalle del día en calendario.html."""
    if request.method == 'POST':
        try:
            c = get_object_or_404(Clase, pk=pk, usuario_id=_uid(request))
            c.satisfaccion = json.loads(request.body).get('satisfaccion', 5)
            c.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'invalid'}, status=405)


def kleit_view(request):
    """Vista principal del chat Kleit. Muestra historial de conversaciones y la sesión activa."""
    if not _login_required(request):
        return redirect('login')
    uid = _uid(request)
    sesiones = SesionKleit.objects.filter(usuario_id=uid).order_by('-updated_at')

    sesion_activa = None
    sesion_pk = request.GET.get('sesion')
    if sesion_pk:
        try:
            sesion_activa = SesionKleit.objects.get(pk=int(sesion_pk), usuario_id=uid)
        except (SesionKleit.DoesNotExist, ValueError):
            pass

    mensajes_parsed = _parsear_mensajes(sesion_activa)

    return render(request, 'kiwi/kleit.html', {
        'sesiones': sesiones,
        'sesion_activa': sesion_activa,
        'mensajes': mensajes_parsed,
        **_ctx(request),
    })


def _parsear_mensajes(sesion):
    """Convierte el JSON de mensajes guardado en objetos listos para el template."""
    if not sesion or not sesion.mensajes:
        return []
    try:
        mensajes_raw = json.loads(sesion.mensajes)
    except Exception:
        return []

    resultado = []
    for msg in mensajes_raw:
        parsed = {
            'role': msg.get('role', 'user'),
            'ts': msg.get('ts', ''),
            'grupo': msg.get('grupo', ''),
        }
        if msg['role'] == 'user':
            parsed['content'] = msg.get('content', '')
        else:
            try:
                content = json.loads(msg.get('content', '{}'))
                ideas_raw = content.get('ideas', [])
                ideas_ids = msg.get('ideas_ids', [])
                parsed['ideas'] = [
                    {**idea, 'db_id': ideas_ids[i] if i < len(ideas_ids) else None}
                    for i, idea in enumerate(ideas_raw)
                ]
                parsed['consejo'] = content.get('consejo_kleit', '')
                parsed['nivel'] = content.get('nivel_detectado', '')
                parsed['categoria'] = content.get('categoria_emocional', '')
                parsed['fuente'] = msg.get('fuente', 'grok')
            except Exception:
                parsed['ideas'] = []
                parsed['consejo'] = msg.get('content', '')
                parsed['fuente'] = 'grok'
        resultado.append(parsed)
    return resultado


def kleit_chat_ajax(request):
    """AJAX POST — recibe {sesion_id?, mensaje, grupo} y retorna respuesta de GROK."""
    if request.method != 'POST':
        return JsonResponse({'error': 'invalid'}, status=405)
    if not _login_required(request):
        return JsonResponse({'error': 'No autenticado'}, status=401)

    uid = _uid(request)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    sesion_id = data.get('sesion_id')
    mensaje_texto = data.get('mensaje', '').strip()
    grupo = data.get('grupo', '').strip()

    if not mensaje_texto:
        return JsonResponse({'error': 'Mensaje vacío'}, status=400)

    # Obtener o crear sesión
    if sesion_id:
        try:
            sesion = SesionKleit.objects.get(pk=int(sesion_id), usuario_id=uid)
        except (SesionKleit.DoesNotExist, ValueError):
            return JsonResponse({'error': 'Sesión no encontrada'}, status=404)
    else:
        sesion = SesionKleit.objects.create(
            usuario_id=uid,
            titulo_sesion=mensaje_texto[:60],
            tema=mensaje_texto[:200],
            grupo=grupo,
            mensajes='[]',
        )

    # Cargar historial de la sesión actual
    try:
        mensajes_sesion = json.loads(sesion.mensajes or '[]')
    except Exception:
        mensajes_sesion = []

    from django.utils import timezone as tz_utils
    ahora = tz_utils.now().isoformat()

    # Construir contenido del mensaje incluyendo grupo de forma natural
    contenido_usuario = mensaje_texto
    if grupo:
        contenido_usuario = f"{mensaje_texto}\n(Grupo objetivo: {grupo})"

    nuevo_msg_user = {
        'role': 'user',
        'content': contenido_usuario,
        'grupo': grupo,
        'ts': ahora,
    }

    # Mensajes para GROK (solo role + content, sin metadatos)
    mensajes_para_grok = [
        {'role': m['role'], 'content': m['content']}
        for m in mensajes_sesion
    ] + [{'role': 'user', 'content': contenido_usuario}]

    # Historial global: todos los títulos de ideas de esta docente
    historial_global = list(
        IdeaKleit.objects.filter(usuario_id=uid).values_list('titulo', flat=True)[:60]
    )

    # Llamar a GROK con el historial completo
    resultado = chat_con_kleit(mensajes_para_grok, historial_global)

    # Guardar ideas nuevas en BD
    ideas_objs = []
    for idea_data in resultado.get('ideas', []):
        expansion = _formatear_expansion(idea_data)
        idea_obj = IdeaKleit.objects.create(
            usuario_id=uid,
            titulo=idea_data.get('titulo', 'Actividad'),
            descripcion=idea_data.get('descripcion', ''),
            expansion=expansion,
            tema_original=mensaje_texto[:200],
            grupo_original=grupo,
            recursos_sugeridos=json.dumps(
                idea_data.get('recursos_digitales', idea_data.get('recursos', [])),
                ensure_ascii=False
            ),
        )
        sesion.ideas.add(idea_obj)
        ideas_objs.append(idea_obj)

    # Contenido del asistente (JSON completo para guardar)
    assistant_content = json.dumps({
        'nivel_detectado': resultado.get('nivel', 'general'),
        'categoria_emocional': resultado.get('categoria', ''),
        'consejo_kleit': resultado.get('consejo', ''),
        'ideas': resultado.get('ideas', []),
    }, ensure_ascii=False)

    nuevo_msg_asistente = {
        'role': 'assistant',
        'content': assistant_content,
        'fuente': resultado.get('fuente', 'gemini'),
        'ts': tz_utils.now().isoformat(),
        'ideas_ids': [idea.pk for idea in ideas_objs],
    }

    # Actualizar sesión
    mensajes_sesion.append(nuevo_msg_user)
    mensajes_sesion.append(nuevo_msg_asistente)
    sesion.mensajes = json.dumps(mensajes_sesion, ensure_ascii=False)
    sesion.tema = mensaje_texto[:200]
    if not sesion.titulo_sesion or sesion.titulo_sesion == 'Nueva conversación':
        sesion.titulo_sesion = mensaje_texto[:60]
    if grupo:
        sesion.grupo = grupo
    sesion.nivel_detectado = resultado.get('nivel', sesion.nivel_detectado)
    sesion.save()

    return JsonResponse({
        'ok': True,
        'sesion_id': sesion.pk,
        'titulo_sesion': sesion.titulo_sesion,
        'respuesta': {
            'consejo': resultado.get('consejo', ''),
            'nivel': resultado.get('nivel', 'general'),
            'categoria': resultado.get('categoria', ''),
            'fuente': resultado.get('fuente', 'gemini'),
            'ideas': resultado.get('ideas', []),
            'ideas_ids': [idea.pk for idea in ideas_objs],
        }
    })


def kleit_eliminar_sesion(request, pk):
    """Elimina una sesión del historial de chat. Soporta POST normal y AJAX."""
    if not _login_required(request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'No autenticado'}, status=401)
        return redirect('login')
    sesion = get_object_or_404(SesionKleit, pk=pk, usuario_id=_uid(request))
    sesion.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True})
    return redirect('kleit')


def _formatear_expansion(idea: dict) -> str:
    """Convierte el dict de una idea (retornado por Gemini o el banco local) a texto
    plano estructurado que se guarda en IdeaKleit.expansion para mostrarse en el template."""
    lineas = []
    if idea.get('duracion_minutos'):
        lineas.append(f"Duracion: {idea['duracion_minutos']} minutos\n")
    if idea.get('materiales'):
        lineas.append("Materiales necesarios:")
        for m in idea['materiales']:
            lineas.append(f"  - {m}")
        lineas.append("")
    if idea.get('pasos'):
        lineas.append("Desarrollo paso a paso:")
        for i, p in enumerate(idea['pasos'], 1):
            lineas.append(f"  {i}. {p}")
        lineas.append("")
    if idea.get('preguntas_reflexion'):
        lineas.append("Preguntas de reflexion:")
        for p in idea['preguntas_reflexion']:
            lineas.append(f"  - {p}")
        lineas.append("")
    if idea.get('indicador_logro'):
        lineas.append(f"Indicador de logro: {idea['indicador_logro']}\n")
    if idea.get('adaptacion_primaria') or idea.get('adaptacion_bachillerato'):
        lineas.append("Adaptaciones:")
        if idea.get('adaptacion_primaria'):
            lineas.append(f"  - Primaria: {idea['adaptacion_primaria']}")
        if idea.get('adaptacion_bachillerato'):
            lineas.append(f"  - Bachillerato: {idea['adaptacion_bachillerato']}")
    return "\n".join(lineas)


def guardar_idea(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'invalid'}, status=405)
    idea = get_object_or_404(IdeaKleit, pk=pk, usuario_id=_uid(request))
    idea.guardada = not idea.guardada
    idea.save()
    return JsonResponse({'guardada': idea.guardada})


def ideas_guardadas_view(request):
    if not _login_required(request):
        return redirect('login')
    uid = _uid(request)
    return render(request, 'kiwi/ideas_guardadas.html', {
        'ideas': IdeaKleit.objects.filter(usuario_id=uid, guardada=True),
        'clases': Clase.objects.filter(usuario_id=uid, completada=False),
        'usuario_nombre': request.session.get('usuario_nombre', 'usuario'),
        'usuario_correo': request.session.get('usuario_correo', ''),
        'usuario_institucion': request.session.get('usuario_institucion', ''),
    })


def asignar_idea_clase(request, pk):
    if request.method == 'POST':
        try:
            idea = get_object_or_404(IdeaKleit, pk=pk)
            idea.usada_en_clase_id = json.loads(request.body).get('clase_id')
            idea.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'invalid'}, status=405)


def recursos_view(request):
    """Lista y crea recursos didácticos. Soporta filtros por ciclo y tipo via query params.
    En POST crea un nuevo Recurso (con archivo opcional en MEDIA_ROOT/recursos/)."""
    if not _login_required(request):
        return redirect('login')
    ciclo_filtro = request.GET.get('ciclo', '')
    tipo_filtro = request.GET.get('tipo', '')

    uid = _uid(request)
    qs = Recurso.objects.filter(usuario_id=uid)
    if ciclo_filtro:
        qs = qs.filter(ciclo=ciclo_filtro)
    if tipo_filtro:
        qs = qs.filter(tipo=tipo_filtro)

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        if titulo:
            Recurso.objects.create(
                usuario_id=uid,
                titulo=titulo,
                ciclo=request.POST.get('ciclo', 'ciclo_uno'),
                tipo=request.POST.get('tipo', 'otro'),
                descripcion=request.POST.get('descripcion', ''),
                enlace=request.POST.get('enlace', ''),
                etiquetas=request.POST.get('etiquetas', ''),
                archivo=request.FILES.get('archivo'),
            )
            messages.success(request, f'Recurso "{titulo}" guardado exitosamente.')
        return redirect('recursos')

    # Estadísticas por ciclo (solo del usuario actual)
    stats = {}
    for ciclo_val, ciclo_label in Recurso.CICLO_CHOICES:
        stats[ciclo_val] = Recurso.objects.filter(usuario_id=uid, ciclo=ciclo_val).count()

    return render(request, 'kiwi/recursos.html', {
        'recursos': qs,
        'ciclos': Recurso.CICLO_CHOICES,
        'tipos': Recurso.TIPO_CHOICES,
        'ciclo_filtro': ciclo_filtro,
        'tipo_filtro': tipo_filtro,
        'stats': stats,
        'usuario_nombre': request.session.get('usuario_nombre', 'usuario'),
        'usuario_correo': request.session.get('usuario_correo', ''),
        'usuario_institucion': request.session.get('usuario_institucion', ''),
    })


def eliminar_recurso(request, pk):
    r = get_object_or_404(Recurso, pk=pk, usuario_id=_uid(request))
    nombre = r.titulo
    r.delete()
    messages.success(request, f'Recurso "{nombre}" eliminado.')
    return redirect('recursos')


def tareas_view(request):
    """Gestiona el CRUD de tareas. El campo POST 'action' determina la operación:
    'create' | 'update_estado' | 'delete'."""
    if not _login_required(request):
        return redirect('login')
    uid = _uid(request)
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'create':
            titulo = request.POST.get('titulo', '').strip()
            if titulo:
                Tarea.objects.create(
                    usuario_id=uid,
                    titulo=titulo, estado=request.POST.get('estado', 'no_empezada'),
                    plazo=request.POST.get('plazo') or None, notas=request.POST.get('notas', ''),
                )
        elif action == 'update_estado':
            t = get_object_or_404(Tarea, pk=request.POST.get('pk'), usuario_id=uid)
            t.estado = request.POST.get('estado', 'no_empezada')
            t.save()
        elif action == 'update':
            t = get_object_or_404(Tarea, pk=request.POST.get('pk'), usuario_id=uid)
            titulo = request.POST.get('titulo', '').strip()
            if titulo:
                t.titulo = titulo
            t.notas = request.POST.get('notas', '')
            t.plazo = request.POST.get('plazo') or None
            t.estado = request.POST.get('estado', t.estado)
            t.save()
        elif action == 'delete':
            get_object_or_404(Tarea, pk=request.POST.get('pk'), usuario_id=uid).delete()
        return redirect('tareas')
    return render(request, 'kiwi/tareas.html', {
        'tareas': Tarea.objects.filter(usuario_id=uid),
        'usuario_nombre': request.session.get('usuario_nombre', 'usuario'),
        'usuario_correo': request.session.get('usuario_correo', ''),
        'usuario_institucion': request.session.get('usuario_institucion', ''),
    })


# ══════════════════════════════════════════════════════════════════
# PLAN DE AULA
# ══════════════════════════════════════════════════════════════════

def plan_aula_view(request):
    if not _login_required(request):
        return redirect('login')
    planes = PlanDeAula.objects.filter(usuario_id=_uid(request))
    return render(request, 'kiwi/plan_aula.html', {
        'planes': planes,
        'grados': PlanDeAula.GRADO_CHOICES,
        'tipos': PlanDeAula.TIPO_CHOICES,
        'periodos': PlanDeAula.PERIODO_CHOICES,
        'competencias_sel': PlanDeAula.COMPETENCIA_SEL_CHOICES,
        'usuario_nombre': request.session.get('usuario_nombre', 'usuario'),
        'usuario_correo': request.session.get('usuario_correo', ''),
        'usuario_institucion': request.session.get('usuario_institucion', ''),
    })


def plan_aula_generar(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if not _login_required(request):
        if is_ajax:
            return JsonResponse({'ok': False, 'error': 'Sesion expirada. Recarga la pagina.'}, status=401)
        return redirect('login')

    if request.method != 'POST':
        return redirect('plan_aula')

    # ── Identificación ──────────────────────────────────────────────────
    titulo      = request.POST.get('titulo', '').strip()
    grado       = request.POST.get('grado', '').strip()
    tipo        = request.POST.get('tipo', 'plan_aula')
    periodo     = request.POST.get('periodo', 'I')
    competencia = request.POST.get('competencia_sel', 'bienestar_integral')
    duracion    = request.POST.get('duracion_semanas', '4')

    # ── Múltiples desempeños ─────────────────────────────────────────────
    try:
        num_desempenios = max(1, min(4, int(request.POST.get('num_desempenios', 1) or 1)))
    except (ValueError, TypeError):
        num_desempenios = 1

    desempenios_input = []
    for i in range(1, num_desempenios + 1):
        d = request.POST.get(f'desempenio_{i}', '').strip()
        if d:
            desempenios_input.append({
                'desempenio': d,
                'temas':      request.POST.get(f'temas_trabajar_{i}', '').strip(),
                'estrategia': request.POST.get(f'estrategia_tipo_{i}', '').strip(),
                'valoracion': request.POST.get(f'valoracion_notas_{i}', '').strip(),
            })

    if not titulo or not grado or not desempenios_input:
        err = 'Completa los campos obligatorios: título, grado y al menos un desempeño.'
        if is_ajax:
            return JsonResponse({'ok': False, 'error': err})
        messages.error(request, err)
        return redirect('plan_aula')

    # ── Generación con IA en paralelo (timeout 110 s compartido) ─────────
    args_list = [
        (titulo, grado, tipo, periodo, competencia,
         di['desempenio'], di['temas'], di['estrategia'], di['valoracion'], duracion)
        for di in desempenios_input
    ]
    contenidos_raw = _generar_todos_con_timeout(args_list, timeout=110)

    desempenios_generados = []
    for di, contenido_str in zip(desempenios_input, contenidos_raw):
        try:
            contenido = json.loads(contenido_str)
        except Exception:
            contenido = {}
        desempenios_generados.append({
            'desempenio':    di['desempenio'],
            'temas':         _parsear_texto_bullets(contenido.get('temas_trabajar', di['temas'])),
            'estrategia':    _parsear_texto_parrafos(contenido.get('estrategia_aprendizaje', '')),
            'valoracion':    _parsear_texto_bullets(contenido.get('valoracion_continua', di['valoracion'])),
            'nivel_superior': contenido.get('nivel_superior', ''),
            'nivel_alto':    contenido.get('nivel_alto', ''),
            'nivel_basico':  contenido.get('nivel_basico', ''),
        })

    # ── Compatibilidad legacy: primer desempeño → campos individuales ────
    primero     = desempenios_input[0]
    primero_gen = desempenios_generados[0]
    contenido_ia_legacy = json.dumps({
        'temas_trabajar':      '\n'.join(primero_gen['temas']),
        'estrategia_aprendizaje': '\n\n'.join(primero_gen['estrategia']),
        'valoracion_continua': '\n'.join(primero_gen['valoracion']),
        'nivel_superior':      primero_gen['nivel_superior'],
        'nivel_alto':          primero_gen['nivel_alto'],
        'nivel_basico':        primero_gen['nivel_basico'],
    }, ensure_ascii=False)

    plan = PlanDeAula.objects.create(
        usuario_id=_uid(request),
        tipo=tipo,
        titulo=titulo,
        grado=grado,
        periodo=periodo,
        metodologia='integrado',
        competencias=competencia,
        objetivo_general=primero['desempenio'],
        contenido_tematico=primero['temas'],
        estrategias=primero['estrategia'],
        evaluacion=primero['valoracion'],
        duracion_semanas=int(duracion) if str(duracion).isdigit() else 4,
        contenido_ia=contenido_ia_legacy,
        desempenios_json=json.dumps(desempenios_generados, ensure_ascii=False),
    )

    if is_ajax:
        return JsonResponse({
            'ok': True,
            'plan_id': plan.pk,
            'titulo': plan.titulo,
            'redirect': f'/plan-aula/{plan.pk}/',
        })

    messages.success(request, f'Plan de aula "{titulo}" generado exitosamente.')
    return redirect('plan_aula_detalle', pk=plan.pk)


def _generar_todos_con_timeout(args_list, timeout=110):
    """Genera contenido IA para múltiples desempeños en paralelo con un timeout compartido."""
    results = [None] * len(args_list)

    def _worker(i, args):
        try:
            results[i] = _generar_plan_con_ia(*args)
        except Exception:
            results[i] = None

    threads = [threading.Thread(target=_worker, args=(i, a), daemon=True)
               for i, a in enumerate(args_list)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout)

    for i, (res, args) in enumerate(zip(results, args_list)):
        if res is None:
            results[i] = _plan_local(*args)
    return results


def plan_aula_detalle(request, pk):
    if not _login_required(request):
        return redirect('login')
    plan = get_object_or_404(PlanDeAula, pk=pk, usuario_id=_uid(request))
    ctx = _contexto_exportar_plan(plan, request)
    ctx['usuario_nombre'] = request.session.get('usuario_nombre', 'usuario')
    ctx['usuario_institucion'] = request.session.get('usuario_institucion', 'Colegio San Francisco de Asís')
    return render(request, 'kiwi/plan_aula_detalle.html', ctx)


def eliminar_plan_aula(request, pk):
    plan = get_object_or_404(PlanDeAula, pk=pk, usuario_id=_uid(request))
    nombre = plan.titulo
    plan.delete()
    messages.success(request, f'Plan "{nombre}" eliminado.')
    return redirect('plan_aula')


def _contexto_exportar_plan(plan, request):
    """Construye el contexto compartido para vistas de exportación del plan."""
    # ── Nuevo formato: múltiples desempeños ──────────────────────────────
    desempenios = []
    if plan.desempenios_json and plan.desempenios_json != '[]':
        try:
            desempenios = json.loads(plan.desempenios_json)
        except Exception:
            pass

    # ── Fallback para planes anteriores sin desempenios_json ─────────────
    if not desempenios:
        contenido = {}
        if plan.contenido_ia:
            try:
                contenido = json.loads(plan.contenido_ia)
            except Exception:
                pass
        desempenios = [{
            'desempenio':    plan.objetivo_general,
            'temas':         _parsear_texto_bullets(contenido.get('temas_trabajar', plan.contenido_tematico)),
            'estrategia':    _parsear_texto_parrafos(contenido.get('estrategia_aprendizaje', '')),
            'valoracion':    _parsear_texto_bullets(contenido.get('valoracion_continua', plan.evaluacion)),
            'nivel_superior': contenido.get('nivel_superior', ''),
            'nivel_alto':    contenido.get('nivel_alto', ''),
            'nivel_basico':  contenido.get('nivel_basico', ''),
        }]

    grado_short_map = {
        'jardin': 'Jardín', 'transicion': 'Transición',
        'primero': '1°', 'segundo': '2°', 'tercero': '3°',
        'cuarto': '4°', 'quinto': '5°', 'sexto': '6°',
        'septimo': '7°', 'octavo': '8°', 'noveno': '9°',
        'decimo': '10°', 'once': '11°',
    }
    ciclo_short_map = {
        'jardin': 'Inicial', 'transicion': 'Inicial',
        'primero': 'I', 'segundo': 'I',
        'tercero': 'II', 'cuarto': 'II', 'quinto': 'II',
        'sexto': 'III', 'septimo': 'III', 'octavo': 'III',
        'noveno': 'IV', 'decimo': 'IV', 'once': 'IV',
    }
    competencia_display_map = {
        'autoconciencia': 'Autoconciencia',
        'autogestion': 'Autogestión',
        'conciencia_social': 'Conciencia Social',
        'habilidades_relacionales': 'Habilidades Relacionales',
        'toma_decisiones': 'Toma de Decisiones',
        'bienestar_integral': 'Bienestar Integral',
    }
    return {
        'plan': plan,
        'desempenios': desempenios,
        'grado_short': grado_short_map.get(plan.grado, plan.grado),
        'ciclo_short': ciclo_short_map.get(plan.grado, plan.ciclo),
        'competencia_display': competencia_display_map.get(plan.competencias, plan.competencias),
        'usuario_nombre': request.session.get('usuario_nombre', '').upper(),
    }


def exportar_plan_pdf(request, pk):
    """Vista de previsualización institucional del Plan de Aula (para imprimir desde el navegador)."""
    if not _login_required(request):
        return redirect('login')
    plan = get_object_or_404(PlanDeAula, pk=pk, usuario_id=_uid(request))
    ctx = _contexto_exportar_plan(plan, request)
    return render(request, 'kiwi/plan_aula_export.html', ctx)


def descargar_plan_pdf(request, pk):
    """Genera y descarga el Plan de Aula como archivo PDF usando xhtml2pdf."""
    if not _login_required(request):
        return redirect('login')
    plan = get_object_or_404(PlanDeAula, pk=pk, usuario_id=_uid(request))
    ctx = _contexto_exportar_plan(plan, request)

    try:
        from xhtml2pdf import pisa
        from django.contrib.staticfiles import finders
        from django.conf import settings as djsettings
        import io, os

        def link_callback(uri, rel):
            if uri.startswith(djsettings.STATIC_URL):
                rel_path = uri[len(djsettings.STATIC_URL):]
                result = finders.find(rel_path)
                if result:
                    return result
            elif uri.startswith(djsettings.MEDIA_URL):
                rel_path = uri[len(djsettings.MEDIA_URL):]
                return os.path.join(djsettings.MEDIA_ROOT, rel_path)
            return uri

        html_string = render_to_string('kiwi/plan_aula_export.html', ctx, request=request)
        pdf_buffer = io.BytesIO()
        result = pisa.CreatePDF(
            html_string.encode('utf-8'),
            dest=pdf_buffer,
            encoding='utf-8',
            link_callback=link_callback,
        )

        if not result.err:
            nombre = f"PlanAula-{plan.titulo[:40]}-{plan.get_grado_display()}.pdf"
            nombre = nombre.replace(' ', '_').replace('/', '-')
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nombre}"'
            return response

        logger.error(f"xhtml2pdf error al generar PDF: {result.err}")
        return render(request, 'kiwi/plan_aula_export.html', ctx)

    except Exception as e:
        logger.error(f"Error al generar PDF: {e}")
        return render(request, 'kiwi/plan_aula_export.html', ctx)


def _parsear_expansion(texto):
    """Parsea el campo expansion de IdeaKleit (generado por _formatear_expansion) a dict estructurado."""
    import re as _re
    result = {
        'duracion': '', 'materiales': [], 'pasos': [],
        'preguntas_reflexion': [], 'indicador_logro': '',
        'adaptacion_primaria': '', 'adaptacion_bachillerato': '',
    }
    current = None
    for raw in (texto or '').split('\n'):
        line = raw.strip()
        if not line:
            continue
        if line.startswith('Duracion:'):
            result['duracion'] = line.replace('Duracion:', '').strip()
        elif line == 'Materiales necesarios:':
            current = 'materiales'
        elif line == 'Desarrollo paso a paso:':
            current = 'pasos'
        elif line == 'Preguntas de reflexion:':
            current = 'preguntas'
        elif line.startswith('Indicador de logro:'):
            result['indicador_logro'] = line.replace('Indicador de logro:', '').strip()
            current = None
        elif line == 'Adaptaciones:':
            current = 'adapt'
        elif current == 'materiales' and line.startswith('- '):
            result['materiales'].append(line[2:])
        elif current == 'preguntas' and line.startswith('- '):
            result['preguntas_reflexion'].append(line[2:])
        elif current == 'pasos' and line:
            m = _re.match(r'^\d+\.\s+(.+)$', line)
            if m:
                result['pasos'].append(m.group(1))
        elif current == 'adapt' and line.startswith('- Primaria:'):
            result['adaptacion_primaria'] = line.replace('- Primaria:', '').strip()
        elif current == 'adapt' and line.startswith('- Bachillerato:'):
            result['adaptacion_bachillerato'] = line.replace('- Bachillerato:', '').strip()
    return result


def exportar_plan_clase_pdf(request, pk):
    """Genera y descarga un Plan de Clase PDF a partir de una idea guardada de Kleit."""
    if not _login_required(request):
        return redirect('login')
    if request.method != 'POST':
        return redirect('ideas_guardadas')

    idea = get_object_or_404(IdeaKleit, pk=pk, usuario_id=_uid(request), guardada=True)

    tema      = request.POST.get('tema', '').strip()
    semana    = request.POST.get('semana', '').strip()
    fecha     = request.POST.get('fecha', '').strip()

    datos = _parsear_expansion(idea.expansion)
    try:
        recursos = json.loads(idea.recursos_sugeridos) if idea.recursos_sugeridos else []
    except Exception:
        recursos = []

    ctx = {
        'idea': idea,
        'tema': tema,
        'semana': semana,
        'fecha': fecha,
        'usuario_nombre': request.session.get('usuario_nombre', ''),
        'datos': datos,
        'recursos': recursos,
    }

    try:
        from xhtml2pdf import pisa
        from django.contrib.staticfiles import finders
        from django.conf import settings as djsettings
        import io, os

        def link_callback(uri, rel):
            if uri.startswith(djsettings.STATIC_URL):
                rel_path = uri[len(djsettings.STATIC_URL):]
                found = finders.find(rel_path)
                if found:
                    return found
            elif uri.startswith(djsettings.MEDIA_URL):
                rel_path = uri[len(djsettings.MEDIA_URL):]
                return os.path.join(djsettings.MEDIA_ROOT, rel_path)
            return uri

        html_string = render_to_string('kiwi/plan_clase_export.html', ctx, request=request)
        pdf_buffer = io.BytesIO()
        result = pisa.CreatePDF(
            html_string.encode('utf-8'),
            dest=pdf_buffer,
            encoding='utf-8',
            link_callback=link_callback,
        )
        if not result.err:
            nombre = f"PlanClase-{idea.titulo[:35]}.pdf".replace(' ', '_').replace('/', '-')
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nombre}"'
            return response

        logger.error(f"xhtml2pdf error plan clase: {result.err}")
    except Exception as e:
        logger.error(f"Error al generar Plan de Clase PDF: {e}")

    return redirect('ideas_guardadas')


def _parsear_texto_bullets(texto):
    """Convierte texto con saltos de línea o guiones en lista de strings."""
    if not texto:
        return []
    items = []
    for linea in texto.split('\n'):
        limpia = linea.strip().lstrip('-•·*▪►→').strip()
        if limpia:
            items.append(limpia)
    return items


def _parsear_texto_parrafos(texto):
    """Divide texto en párrafos por doble salto de línea; si no los hay, por línea simple."""
    if not texto:
        return []
    bloques = [b.strip() for b in texto.split('\n\n') if b.strip()]
    if not bloques:
        bloques = [l.strip() for l in texto.split('\n') if l.strip()]
    return bloques or [texto.strip()]


def _generar_plan_con_ia(titulo, grado, tipo, periodo, competencia, desempenio,
                        temas_trabajar, estrategia_tipo, valoracion_notas, duracion):
    """
    Genera el contenido del plan de aula con Gemini REST API directa.
    """
    import urllib.request
    import urllib.error
    from django.conf import settings

    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key or api_key == 'PEGA_AQUI_TU_API_KEY':
        return _plan_local(titulo, grado, tipo, periodo, competencia, desempenio,
                           temas_trabajar, estrategia_tipo, valoracion_notas, duracion)

    model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash')
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model_name}:generateContent?key={api_key}"
    )

    grado_desc       = dict(PlanDeAula.GRADO_CHOICES).get(grado, grado)
    competencia_desc = dict(PlanDeAula.COMPETENCIA_SEL_CHOICES).get(competencia, competencia)
    tipo_desc        = 'Plan de Aula' if tipo == 'plan_aula' else 'Pensum / Malla Curricular'

    extras = []
    if temas_trabajar:
        extras.append(f"- Temas sugeridos por el docente: {temas_trabajar}")
    if estrategia_tipo:
        extras.append(f"- Estrategia preferida: {estrategia_tipo}")
    if valoracion_notas:
        extras.append(f"- Nota de evaluación: {valoracion_notas}")
    extras_txt = "\n".join(extras) if extras else ""

    prompt = f"""
Eres un experto en educación socioemocional (SEL) para el contexto colombiano.
Debes generar el contenido de un {tipo_desc} para el Colegio San Francisco de Asís (Cali, Colombia),
siguiendo exactamente el formato institucional del colegio.

INFORMACIÓN DEL PLAN:
- Campo de Formación: Gestión Socioemocional y Bienestar
- Competencia SEL: {competencia_desc}
- Grado: {grado_desc}
- Período: {periodo}
- Duración: {duracion} semanas
- DESEMPEÑO (¿Qué logrará el estudiante?): {desempenio}
{extras_txt}

Fundamenta todo el contenido en los marcos CASEL, Yale RULER, Seligman PERMA,
Kabat-Zinn MBSR, Rosenberg CNV, APA e ICBF Colombia.

Genera el JSON con esta estructura EXACTA (sin texto extra):
{{
  "temas_trabajar": "Lista clara de los temas y subtemas que se abordarán, separados por salto de línea. Adapta al nivel {grado_desc}.",
  "estrategia_aprendizaje": "Texto completo de la estrategia de aprendizaje (¿Cómo?). Debe incluir: cómo inicia el docente, desarrollo paso a paso con actividades concretas, estrategias didácticas activas (dinámicas, herramientas, trabajo grupal) y cierre de la clase. Redactar en 3er persona (El docente...). Adaptar al nivel {grado_desc}. Mínimo 200 palabras.",
  "valoracion_continua": "Descripción completa de la valoración continua: instrumentos de evaluación (talleres, evaluaciones, actitud, portafolio emocional, etc.), criterios y política de mejoramiento. Adaptar al área de gestión socioemocional.",
  "nivel_superior": "Descripción de qué demuestra un estudiante en nivel SUPERIOR para este desempeño. Una oración clara y precisa.",
  "nivel_alto": "Descripción de qué demuestra un estudiante en nivel ALTO para este desempeño. Una oración clara y precisa.",
  "nivel_basico": "Descripción de qué demuestra un estudiante en nivel BÁSICO para este desempeño. Una oración clara y precisa."
}}

Responde SOLO con el JSON válido, sin markdown ni texto adicional.
"""

    try:
        payload = {
            'contents': [{'role': 'user', 'parts': [{'text': prompt}]}],
            'generationConfig': {
                'response_mime_type': 'application/json',
                'temperature': 0.7,
            },
        }
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(url, data=body, method='POST')
        req.add_header('Content-Type', 'application/json')

        with urllib.request.urlopen(req, timeout=110) as resp:
            data = json.loads(resp.read())

        raw = data['candidates'][0]['content']['parts'][0]['text'].strip()
        if raw.startswith('```'):
            parte = raw.split('```')[1]
            raw = parte[4:] if parte.startswith('json') else parte
        raw = raw.strip().rstrip('`').strip()
        parsed = json.loads(raw)
        return json.dumps(parsed, ensure_ascii=False)

    except Exception as e:
        logger.error(f"_generar_plan_con_ia error: {type(e).__name__}: {e}")
        return _plan_local(titulo, grado, tipo, periodo, competencia, desempenio,
                           temas_trabajar, estrategia_tipo, valoracion_notas, duracion)



def _plan_local(titulo, grado, tipo, periodo, competencia, desempenio,
                temas_trabajar, estrategia_tipo, valoracion_notas, duracion):
    """Fallback cuando Gemini no está disponible — sigue el formato del colegio."""
    dur = int(duracion) if str(duracion).isdigit() else 4
    grado_desc = dict(PlanDeAula.GRADO_CHOICES).get(grado, grado)

    temas_base = temas_trabajar if temas_trabajar else (
        "- Reconocimiento y vocabulario emocional\n"
        "- Autorregulación: técnicas de manejo emocional\n"
        "- Empatía y comunicación asertiva\n"
        "- Resolución de conflictos y toma de decisiones\n"
        "- Proyecto integrador de bienestar personal"
    )

    estrategia_base = (
        f"El docente iniciará la clase con un check-in emocional de 5 minutos, "
        f"invitando a los estudiantes de {grado_desc} a identificar su estado emocional "
        f"usando la rueda de emociones de Plutchik. Este momento de apertura crea un "
        f"ambiente seguro y de confianza para el trabajo socioemocional.\n\n"
        f"Posteriormente, el docente presentará el tema central relacionado con '{desempenio}', "
        f"utilizando situaciones cotidianas y contextos cercanos a los estudiantes para "
        f"hacer el aprendizaje significativo y relevante.\n\n"
        f"Durante el desarrollo de la clase, se emplearán estrategias didácticas activas como "
        f"{'el ' + estrategia_tipo + ',' if estrategia_tipo else ''} círculos de diálogo "
        f"socioemocional, dinámicas grupales y técnicas de mindfulness adaptadas al nivel "
        f"{grado_desc}. Los estudiantes participarán en actividades vivenciales que les "
        f"permitan reflexionar, practicar y aplicar las habilidades socioemocionales.\n\n"
        f"Para el cierre, los estudiantes registrarán sus aprendizajes en el diario emocional "
        f"personal y compartirán un compromiso concreto para aplicar lo aprendido en su vida "
        f"cotidiana. El docente reforzará los conceptos clave y abrirá un espacio de preguntas."
    )

    valoracion_base = valoracion_notas if valoracion_notas else (
        "Se calificarán talleres programados en clase, actitud para el aprendizaje y "
        "participación activa en las dinámicas socioemocionales. La valoración será continua "
        "e incluirá: portafolio emocional del estudiante, rúbricas de participación, "
        "autoevaluación semanal y observación directa del docente.\n\n"
        "De presentarse dificultades en el proceso, se desarrollarán actividades de "
        "mejoramiento basadas en el acompañamiento personalizado y la reflexión guiada."
    )

    data = {
        "temas_trabajar": temas_base,
        "estrategia_aprendizaje": estrategia_base,
        "valoracion_continua": valoracion_base,
        "nivel_superior": (
            f"Demuestra comprensión profunda del desempeño, aplica las habilidades "
            f"socioemocionales en contextos variados y argumenta sus reflexiones con "
            f"claridad, evidenciando un alto nivel de autoconciencia y empatía."
        ),
        "nivel_alto": (
            f"Alcanza el desempeño propuesto, aplica las estrategias socioemocionales "
            f"trabajadas en clase y participa activamente en las dinámicas, relacionando "
            f"el aprendizaje con situaciones de su vida cotidiana."
        ),
        "nivel_basico": (
            f"Reconoce los conceptos fundamentales del desempeño e identifica las "
            f"emociones y habilidades trabajadas, con apoyo del docente y de sus pares."
        ),
    }
    return json.dumps(data, ensure_ascii=False)


# ══════════════════════════════════════════════════════════════════
# APIS
# ══════════════════════════════════════════════════════════════════

def api_clases_proximas(request):
    ahora = timezone.now()
    en_15min = ahora + timedelta(minutes=15)
    clases = Clase.objects.filter(usuario_id=_uid(request), fecha__gte=ahora, fecha__lte=en_15min, completada=False)
    return JsonResponse({'clases': [
        {'id': c.pk, 'titulo': c.titulo, 'grupo': c.grupo,
         'hora': c.fecha.strftime('%H:%M'),
         'minutos': max(0, int((c.fecha - ahora).total_seconds() / 60))}
        for c in clases
    ]})


def api_clases_json(request):
    return JsonResponse([
        {
            'id': c.pk,
            'title': f"{c.titulo} ({c.grupo})",
            'start': c.fecha.isoformat(),
            'color': '#6a80e2' if not c.completada else '#4caf50',
            'es_recurrente': c.es_recurrente,
            'clase_padre': c.clase_padre_id,
        }
        for c in Clase.objects.filter(usuario_id=_uid(request))
    ], safe=False)


def api_estado_kleit(request):
    from django.conf import settings
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    activo = bool(api_key)
    modelo = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash') if activo else None
    return JsonResponse({
        'gemini_activo': activo,
        'modelo': modelo,
        'mensaje': 'Gemini IA activa' if activo else 'Usando banco local',
    })


def perfil_view(request):
    """Actualiza nombre, correo, institución y foto en la sesión activa."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        institucion = request.POST.get('institucion', '').strip()
        if nombre:
            request.session['usuario_nombre'] = nombre
        if correo:
            request.session['usuario_correo'] = correo
        if institucion:
            request.session['usuario_institucion'] = institucion
        if 'foto' in request.FILES:
            import os
            from django.conf import settings as djsettings
            foto = request.FILES['foto']
            ext = foto.name.rsplit('.', 1)[-1].lower()
            if ext in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                uid = request.session.get('usuario_id', 'anon')
                filename = f"avatar_{uid}.{ext}"
                avatars_dir = os.path.join(djsettings.MEDIA_ROOT, 'avatars')
                os.makedirs(avatars_dir, exist_ok=True)
                filepath = os.path.join(avatars_dir, filename)
                with open(filepath, 'wb') as f:
                    for chunk in foto.chunks():
                        f.write(chunk)
                request.session['usuario_foto'] = f"{djsettings.MEDIA_URL}avatars/{filename}"
        request.session.modified = True
        messages.success(request, 'Perfil actualizado correctamente.')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


# ══════════════════════════════════════════════════════════════════
# GOOGLE CALENDAR
# ══════════════════════════════════════════════════════════════════

from . import google_calendar as gcal
from . import psicologia_db


def google_auth_start(request):
    if not _login_required(request):
        return redirect('login')
    try:
        auth_url = gcal.get_auth_url(request)
        return redirect(auth_url)
    except ValueError as e:
        messages.error(request, f'{e} — Configura GOOGLE_CLIENT_ID en tu archivo .env')
        return redirect('calendario')


def google_auth_callback(request):
    """Recibe el code de OAuth2 de Google, intercambia por tokens y los guarda en sesión.
    NOTA: los tokens NO se persisten en BD — se pierden si la sesión expira."""
    if not _login_required(request):
        return redirect('login')
    error = request.GET.get('error')
    if error:
        messages.error(request, f'Google Calendar: acceso denegado ({error})')
        return redirect('calendario')
    code = request.GET.get('code')
    if not code:
        messages.error(request, 'No se recibió código de autorización de Google.')
        return redirect('calendario')
    tokens = gcal.exchange_code_for_tokens(request, code)
    if not tokens or 'access_token' not in tokens:
        messages.error(request, 'Error al conectar con Google Calendar. Intenta de nuevo.')
        return redirect('calendario')
    import time
    request.session['google_access_token'] = tokens.get('access_token')
    request.session['google_refresh_token'] = tokens.get('refresh_token')
    request.session['google_token_expires'] = int(time.time()) + tokens.get('expires_in', 3600)
    request.session['google_connected'] = True
    request.session.modified = True
    uid = request.session.get('usuario_id')
    if uid and tokens.get('refresh_token'):
        try:
            u = Usuario.objects.get(pk=uid)
            u.google_refresh_token = tokens['refresh_token']
            u.save()
        except Usuario.DoesNotExist:
            pass
    messages.success(request, 'Google Calendar conectado exitosamente.')
    return redirect('calendario')


def google_disconnect(request):
    if not _login_required(request):
        return redirect('login')
    uid = request.session.get('usuario_id')
    if uid:
        try:
            u = Usuario.objects.get(pk=uid)
            u.google_refresh_token = ''
            u.save()
        except Usuario.DoesNotExist:
            pass
    gcal.desconectar_google(request.session)
    messages.success(request, 'Google Calendar desconectado.')
    return redirect('calendario')


def google_sync_clase(request, pk):
    if not _login_required(request):
        return JsonResponse({'error': 'No autenticado'}, status=401)
    if not gcal.is_connected(request.session):
        return JsonResponse({'error': 'Google Calendar no conectado'}, status=403)
    clase = get_object_or_404(Clase, pk=pk)
    if clase.google_event_id:
        ok = gcal.actualizar_evento_google(request.session, clase)
        if ok:
            return JsonResponse({'ok': True, 'accion': 'actualizado', 'event_id': clase.google_event_id})
        return JsonResponse({'error': 'No se pudo actualizar el evento'}, status=500)
    else:
        event_id = gcal.crear_evento_google(request.session, clase)
        if event_id:
            clase.google_event_id = event_id
            clase.save()
            return JsonResponse({'ok': True, 'accion': 'creado', 'event_id': event_id})
        return JsonResponse({'error': 'No se pudo crear el evento'}, status=500)


def google_sync_todas(request):
    if not _login_required(request):
        return redirect('login')
    if not gcal.is_connected(request.session):
        messages.error(request, 'Primero conecta Google Calendar.')
        return redirect('calendario')
    clases = Clase.objects.filter(usuario_id=_uid(request), completada=False)
    creadas = actualizadas = errores = 0
    for clase in clases:
        if clase.google_event_id:
            if gcal.actualizar_evento_google(request.session, clase):
                actualizadas += 1
            else:
                errores += 1
        else:
            event_id = gcal.crear_evento_google(request.session, clase)
            if event_id:
                clase.google_event_id = event_id
                clase.save()
                creadas += 1
            else:
                errores += 1
    msg = f'Sincronizacion completa: {creadas} creadas, {actualizadas} actualizadas.'
    if errores:
        msg += f' {errores} errores.'
    messages.success(request, msg)
    return redirect('calendario')


def api_google_eventos(request):
    if not _login_required(request):
        return JsonResponse({'error': 'No autenticado'}, status=401)
    if not gcal.is_connected(request.session):
        return JsonResponse({'conectado': False, 'eventos': []})
    eventos = gcal.listar_eventos_google(request.session, dias=30)
    return JsonResponse({
        'conectado': True,
        'eventos': [
            {
                'id': e.get('id'),
                'titulo': e.get('summary', 'Sin titulo'),
                'inicio': e.get('start', {}).get('dateTime', e.get('start', {}).get('date')),
                'fin': e.get('end', {}).get('dateTime', e.get('end', {}).get('date')),
            }
            for e in eventos
        ]
    })


def api_frase_dia(request):
    frase = psicologia_db.obtener_frase_del_dia()
    return JsonResponse(frase)
