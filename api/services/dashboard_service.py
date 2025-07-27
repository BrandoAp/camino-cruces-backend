from django.db.models import Count
from django.utils import timezone
from datetime import date, datetime, timedelta
import pytz
from ..models import RegistroVisita, Visitante, Encuesta


def obtener_timezone_panama():
    """
    Retorna la zona horaria de Panamá.
    """
    return pytz.timezone('America/Panama')


def obtener_fecha_actual_panama():
    """
    Obtiene la fecha actual en la zona horaria de Panamá.
    """
    tz_panama = obtener_timezone_panama()
    ahora_panama = timezone.now().astimezone(tz_panama)
    return ahora_panama.date()


def obtener_rango_dia_panama(fecha=None):
    """
    Obtiene el rango completo del día en zona horaria de Panamá.
    Si no se proporciona fecha, usa el día actual de Panamá.
    
    Returns:
        tuple: (inicio_dia_utc, fin_dia_utc) en UTC para consultas a la BD
    """
    if fecha is None:
        fecha = obtener_fecha_actual_panama()
    
    tz_panama = obtener_timezone_panama()
    
    # Crear inicio del día en Panamá (00:00:00)
    inicio_dia_panama = tz_panama.localize(
        datetime.combine(fecha, datetime.min.time())
    )
    
    # Crear fin del día en Panamá (23:59:59.999999)
    fin_dia_panama = tz_panama.localize(
        datetime.combine(fecha, datetime.max.time())
    )
    
    # Convertir a UTC para las consultas a la base de datos
    inicio_dia_utc = inicio_dia_panama.astimezone(pytz.UTC)
    fin_dia_utc = fin_dia_panama.astimezone(pytz.UTC)
    
    return inicio_dia_utc, fin_dia_utc


def obtener_visitas_recientes():
    """
    Obtiene las visitas recientes con toda la información necesaria.
    Retorna: Fecha, Nombre, Adulto, Niño, Nacionalidad, Motivo de Visita, Sendero, Hora de Entrada, Teléfono
    """
    visitas = RegistroVisita.objects.select_related('visitante').order_by('-fecha_visita')[:50]  # Últimas 50 visitas
    
    tz_panama = obtener_timezone_panama()
    visitas_data = []
    
    for visita in visitas:
        visitante = visita.visitante
        
        # Convertir fecha y hora a zona horaria de Panamá para mostrar
        fecha_panama = visita.fecha_visita.astimezone(tz_panama)
        hora_panama = visita.hora_entrada
        
        # Si hora_entrada es timezone-aware, convertir a Panamá
        if timezone.is_aware(hora_panama):
            # Crear datetime completo para convertir zona horaria
            datetime_completo = datetime.combine(fecha_panama.date(), hora_panama.time())
            datetime_completo = timezone.make_aware(datetime_completo, pytz.UTC)
            hora_panama = datetime_completo.astimezone(tz_panama).time()
        
        # Determinar si es adulto o niño
        es_adulto = visitante.adulto_nino.lower() == 'adulto'
        adulto_count = 1 if es_adulto else 0
        nino_count = 1 if not es_adulto else 0
        
        visita_info = {
            'fecha': fecha_panama.strftime('%Y-%m-%d'),
            'nombre': visitante.nombre_visitante,
            'adulto': adulto_count,
            'nino': nino_count,
            'nacionalidad': visitante.nacionalidad,
            'motivo_visita': visita.razon_visita,
            'sendero': visita.sendero_visitado,
            'hora_entrada': hora_panama.strftime('%H:%M:%S'),
            'telefono': visitante.telefono
        }
        visitas_data.append(visita_info)
    
    return visitas_data


def contar_visitantes_hoy():
    """
    Cuenta el número de visitantes que han llegado HOY en zona horaria de Panamá.
    Retorna: número entero
    """
    inicio_dia_utc, fin_dia_utc = obtener_rango_dia_panama()
    
    # Debug: Imprimir rangos para verificar
    tz_panama = obtener_timezone_panama()
    print(f"[DEBUG] Contando visitantes para el día: {obtener_fecha_actual_panama()}")
    print(f"[DEBUG] Rango UTC: {inicio_dia_utc} - {fin_dia_utc}")
    print(f"[DEBUG] Rango Panamá: {inicio_dia_utc.astimezone(tz_panama)} - {fin_dia_utc.astimezone(tz_panama)}")
    
    count = RegistroVisita.objects.filter(
        fecha_visita__gte=inicio_dia_utc,
        fecha_visita__lte=fin_dia_utc
    ).count()
    
    print(f"[DEBUG] Visitantes encontrados: {count}")
    return count


def contar_encuestas_hoy():
    """
    Cuenta el número de encuestas llenadas HOY en zona horaria de Panamá.
    Retorna: número entero
    """
    inicio_dia_utc, fin_dia_utc = obtener_rango_dia_panama()
    
    # Debug: Imprimir rangos para verificar
    tz_panama = obtener_timezone_panama()
    print(f"[DEBUG] Contando encuestas para el día: {obtener_fecha_actual_panama()}")
    print(f"[DEBUG] Rango UTC: {inicio_dia_utc} - {fin_dia_utc}")
    print(f"[DEBUG] Rango Panamá: {inicio_dia_utc.astimezone(tz_panama)} - {fin_dia_utc.astimezone(tz_panama)}")
    
    count = Encuesta.objects.filter(
        fecha_visita__gte=inicio_dia_utc,
        fecha_visita__lte=fin_dia_utc
    ).count()
    
    print(f"[DEBUG] Encuestas encontradas: {count}")
    return count


def obtener_visitantes_por_pais():
    """
    Obtiene el conteo de visitantes agrupados por país/nacionalidad.
    Retorna: lista de diccionarios con 'pais' y 'cantidad'
    """
    # Necesitamos hacer una consulta que agrupe por nacionalidad
    # Como nacionalidad está encriptada, tenemos que obtener todos los visitantes
    # y agruparlos manualmente después de desencriptar
    
    visitantes = Visitante.objects.all()
    paises_count = {}
    
    for visitante in visitantes:
        nacionalidad = visitante.nacionalidad
        if nacionalidad in paises_count:
            paises_count[nacionalidad] += 1
        else:
            paises_count[nacionalidad] = 1
    
    # Convertir a lista de diccionarios y ordenar por cantidad descendente
    resultado = []
    for pais, cantidad in paises_count.items():
        resultado.append({
            'pais': pais,
            'cantidad': cantidad
        })
    
    # Ordenar por cantidad descendente
    resultado.sort(key=lambda x: x['cantidad'], reverse=True)
    
    return resultado


def obtener_visitantes_por_sendero():
    """
    Obtiene el conteo de visitantes agrupados por sendero visitado.
    Retorna: lista de diccionarios con 'sendero' y 'cantidad'
    """
    # Agrupar por sendero visitado
    senderos_count = {}
    visitas = RegistroVisita.objects.all()
    
    for visita in visitas:
        sendero = visita.sendero_visitado
        if sendero in senderos_count:
            senderos_count[sendero] += 1
        else:
            senderos_count[sendero] = 1
    
    # Convertir a lista de diccionarios y ordenar por cantidad descendente
    resultado = []
    for sendero, cantidad in senderos_count.items():
        resultado.append({
            'sendero': sendero,
            'cantidad': cantidad
        })
    
    # Ordenar por cantidad descendente
    resultado.sort(key=lambda x: x['cantidad'], reverse=True)
    
    return resultado


# ===========================
# FUNCIONES ADICIONALES DE DEBUG Y UTILIDAD
# ===========================

def debug_timezone_info():
    """
    Función de debug para verificar información de zona horaria.
    """
    from django.conf import settings
    
    tz_panama = obtener_timezone_panama()
    ahora_utc = timezone.now()
    ahora_panama = ahora_utc.astimezone(tz_panama)
    fecha_panama = obtener_fecha_actual_panama()
    
    print(f"=== DEBUG TIMEZONE INFO ===")
    print(f"Django TIME_ZONE setting: {settings.TIME_ZONE}")
    print(f"Django USE_TZ setting: {settings.USE_TZ}")
    print(f"UTC actual: {ahora_utc}")
    print(f"Panamá actual: {ahora_panama}")
    print(f"Fecha Panamá: {fecha_panama}")
    print(f"==============================")
    
    return {
        'utc_now': ahora_utc,
        'panama_now': ahora_panama,
        'panama_date': fecha_panama,
        'timezone_setting': settings.TIME_ZONE,
        'use_tz': settings.USE_TZ
    }


def contar_visitantes_fecha_especifica(fecha_str):
    """
    Cuenta visitantes de una fecha específica en formato YYYY-MM-DD.
    Útil para debugging y verificación.
    """
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        inicio_dia_utc, fin_dia_utc = obtener_rango_dia_panama(fecha)
        
        count = RegistroVisita.objects.filter(
            fecha_visita__gte=inicio_dia_utc,
            fecha_visita__lte=fin_dia_utc
        ).count()
        
        print(f"[DEBUG] Visitantes en {fecha_str}: {count}")
        return count
        
    except ValueError:
        print(f"[ERROR] Formato de fecha inválido: {fecha_str}. Use YYYY-MM-DD")
        return 0


def listar_visitas_hoy_debug():
    """
    Lista todas las visitas de hoy con información detallada para debug.
    """
    inicio_dia_utc, fin_dia_utc = obtener_rango_dia_panama()
    
    visitas = RegistroVisita.objects.filter(
        fecha_visita__gte=inicio_dia_utc,
        fecha_visita__lte=fin_dia_utc
    ).select_related('visitante').order_by('fecha_visita')
    
    tz_panama = obtener_timezone_panama()
    
    print(f"=== VISITAS DE HOY ({obtener_fecha_actual_panama()}) ===")
    for visita in visitas:
        fecha_panama = visita.fecha_visita.astimezone(tz_panama)
        print(f"ID: {visita.id} | Visitante: {visita.visitante.nombre_visitante} | "
              f"Fecha UTC: {visita.fecha_visita} | Fecha Panamá: {fecha_panama}")
    print(f"Total: {visitas.count()} visitas")
    print("=" * 50)
    
    return list(visitas)