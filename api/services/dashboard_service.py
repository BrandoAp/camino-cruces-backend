from django.db.models import Count
from django.utils import timezone
from datetime import date
from datetime import *
from ..models import RegistroVisita, Visitante, Encuesta


def obtener_visitas_recientes():
    """
    Obtiene las visitas recientes con toda la información necesaria.
    Retorna: Fecha, Nombre, Adulto, Niño, Nacionalidad, Motivo de Visita, Sendero, Hora de Entrada, Teléfono
    """
    visitas = RegistroVisita.objects.select_related('visitante').order_by('-fecha_visita')[:50]  # Últimas 50 visitas
    
    visitas_data = []
    for visita in visitas:
        visitante = visita.visitante
        
        # Determinar si es adulto o niño
        es_adulto = visitante.adulto_nino.lower() == 'adulto'
        adulto_count = 1 if es_adulto else 0
        nino_count = 1 if not es_adulto else 0
        
        visita_info = {
            'fecha': visita.fecha_visita.strftime('%Y-%m-%d'),
            'nombre': visitante.nombre_visitante,
            'adulto': adulto_count,
            'nino': nino_count,
            'nacionalidad': visitante.nacionalidad,
            'motivo_visita': visita.razon_visita,
            'sendero': visita.sendero_visitado,
            'hora_entrada': visita.hora_entrada.strftime('%H:%M:%S'),
            'telefono': visitante.telefono
        }
        visitas_data.append(visita_info)
    
    return visitas_data


def contar_visitantes_hoy():
    """
    Cuenta el número de visitantes que han llegado hoy.
    Retorna: número entero
    """
    from django.utils import timezone
    
    hoy = date.today()
    
    # Crear el rango de fechas para todo el día
    inicio_dia = timezone.make_aware(
        datetime.combine(hoy, datetime.min.time())
    )
    fin_dia = timezone.make_aware(
        datetime.combine(hoy, datetime.max.time())
    )
    
    queryset = RegistroVisita.objects.filter(
        fecha_visita__gte=inicio_dia,
        fecha_visita__lt=fin_dia + timedelta(days=1)
    )
    
    count = queryset.count()
    return count


def contar_encuestas_hoy():
    """
    Cuenta el número de encuestas llenadas hoy.
    Retorna: número entero
    """
    from django.utils import timezone
    from datetime import date, datetime, timedelta
    
    hoy = date.today()
    
    # Crear el rango de fechas para todo el día
    inicio_dia = timezone.make_aware(
        datetime.combine(hoy, datetime.min.time())
    )
    fin_dia = timezone.make_aware(
        datetime.combine(hoy, datetime.max.time())
    )
    
    queryset = Encuesta.objects.filter(
        fecha_visita__gte=inicio_dia,
        fecha_visita__lt=fin_dia + timedelta(days=1)
    )
    
    count = queryset.count()
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