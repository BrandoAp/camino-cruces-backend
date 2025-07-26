from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from django.http import HttpResponse
from .services.reporte_excel import generar_reporte_completo

from .models import Visitante, RegistroVisita, Sendero
from .serializers import (UsuarioSerializer, SenderoSerializer, SenderoFotoSerializer, VisitanteSerializer, ComentarioSerializer)
from .services import usuario_service, sendero_service, foto_sendero_service, dashboard_service, comentario_service, valoracion_service, encuesta_service

    
class VisitanteViewSet(viewsets.ModelViewSet):
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer

# ==============================
# Samir
# ==============================
@api_view(['POST'])
def registro_usuario(request):
    """Crea un usuario nuevo."""
    usuario = usuario_service.registrar_usuario(request.data)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def obtener_usuario(request, id):
    """Obtiene un usuario por ID."""
    usuario = usuario_service.obtener_usuario(id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)


@api_view(['GET'])
def mostrar_sendero(request, id):
    """Devuelve la información de un sendero."""
    sendero = sendero_service.obtener_sendero(id)
    serializer = SenderoSerializer(sendero)
    return Response(serializer.data)


@api_view(['GET'])
def listar_senderos(request):
    """Devuelve todos los senderos."""
    senderos = sendero_service.listar_todos_los_senderos()
    serializer = SenderoSerializer(senderos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def mostrar_foto_sendero(request, id):
    """Devuelve la foto de un sendero específico."""
    foto = foto_sendero_service.obtener_foto_sendero(id)
    serializer = SenderoFotoSerializer(foto)
    return Response(serializer.data)


@api_view(['GET'])
def listar_fotos_senderos(request):
    """Devuelve todas las fotos de senderos."""
    fotos = foto_sendero_service.obtener_todas_fotos_sendero()
    serializer = SenderoFotoSerializer(fotos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def login_usuario(request):
    email = request.data.get("email")
    contraseña = request.data.get("contraseña")

    datos, error = usuario_service.autenticar_usuario(email, contraseña)

    if error:
        return Response({"detail": error}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(datos, status=status.HTTP_200_OK)


@api_view(['POST'])
def registrar_encuesta_view(request):
    data = request.data
    encuesta, error = encuesta_service.registrar_encuesta(data)

    if error:
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'mensaje': 'Encuesta registrada correctamente'}, status=status.HTTP_201_CREATED)



#endpoints de comentarios(Javier)
@api_view(['POST'])
def agregar_comentario(request):
    data = request.data.copy()
    serializer = ComentarioSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    comentario = serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def comentarios_por_sendero(request, sendero_id):
    """ Devuelve todos los comentarios asociados a un sendero específico"""
    comentarios = comentario_service.listar_comentarios_por_sendero(sendero_id)
    serializer = ComentarioSerializer(comentarios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def valoracion_promedio(request, sendero_id):
    """Calcula y devuelve la valoración promedio de los comentarios de un sendero específico."""
    promedio = valoracion_service.obtener_valoracion_promedio(sendero_id)
    return Response({
        "sendero_id": sendero_id,
        "valoracion_promedio": promedio
    })

@api_view(['GET'])
def valoraciones_por_sendero(request, sendero_id):
    data = valoracion_service.obtener_valoraciones_por_sendero(sendero_id)
    return Response(data)

# ==============================
# RELEZ
# ==============================

@api_view(['GET'])
def obtener_visitante_por_cedula(request, cedula):
    visitante = Visitante.objects.filter(cedula_pasaporte=cedula).first()
    if visitante:
        serializer = VisitanteSerializer(visitante)
        return Response(serializer.data)
    return Response({"detail": "Visitante no encontrado."}, status=404)


@api_view(['POST'])
def registrar_visita(request):
    cedula = request.data.get("cedula_pasaporte")
    sendero_nombre = request.data.get("sendero_visitado")
    razon = request.data.get("razon_visita")

    if not cedula or not sendero_nombre or not razon:
        return Response({"detail": "Faltan datos requeridos."}, status=400)

    visitante = Visitante.objects.filter(cedula_pasaporte=cedula).first()
    if not visitante:
        return Response({"detail": "Visitante no encontrado."}, status=404)

    # ✅ Verificar que el sendero exista
    sendero = Sendero.objects.filter(nombre_sendero=sendero_nombre).first()
    if not sendero:
        return Response({"detail": "El sendero no existe."}, status=400)

    # Ahora sí guardar
    visita = RegistroVisita.objects.create(
        visitante=visitante,
        sendero_visitado=sendero.nombre_sendero,
        razon_visita=razon
    )

    return Response({"mensaje": "Visita registrada correctamente."}, status=201)



@api_view(['POST'])
def registrar_visitante_y_visita(request):
    data = request.data

    campos_obligatorios = [
        "cedula_pasaporte", "nombre_visitante", "nacionalidad", "adulto_nino",
        "telefono", "genero", "sendero_visitado", "razon_visita"
    ]

    # Validar campos vacíos
    for campo in campos_obligatorios:
        if campo not in data or not data[campo]:
            return Response({"detail": f"Campo '{campo}' es requerido."}, status=400)

    # Verificar que el sendero exista
    sendero_nombre = data["sendero_visitado"]
    sendero = Sendero.objects.filter(nombre_sendero=sendero_nombre).first()
    if not sendero:
        return Response({"detail": "El sendero no existe."}, status=400)

    # Validar si ya existe el visitante
    if Visitante.objects.filter(cedula_pasaporte=data["cedula_pasaporte"]).exists():
        return Response({"detail": "El visitante ya está registrado."}, status=400)

    # Crear visitante
    visitante = Visitante.objects.create(
        cedula_pasaporte=data["cedula_pasaporte"],
        nombre_visitante=data["nombre_visitante"],
        nacionalidad=data["nacionalidad"],
        adulto_nino=data["adulto_nino"],
        telefono=data["telefono"],
        genero=data["genero"]
    )

    # Crear visita asociada
    RegistroVisita.objects.create(
        visitante=visitante,
        sendero_visitado=sendero.nombre_sendero,
        razon_visita=data["razon_visita"]
    )

    return Response({"mensaje": "Visitante y visita registrados correctamente."}, status=201)

@api_view(['POST'])
def registrar_visita_por_id(request):
    visitante_id = request.data.get("visitante_id")
    sendero_nombre = request.data.get("sendero_visitado")
    razon = request.data.get("razon_visita")

    if not visitante_id or not sendero_nombre or not razon:
        return Response({"detail": "Faltan datos requeridos."}, status=400)

    try:
        visitante = Visitante.objects.get(id=visitante_id)
    except Visitante.DoesNotExist:
        return Response({"detail": "Visitante no encontrado."}, status=404)

    sendero = Sendero.objects.filter(nombre_sendero=sendero_nombre).first()
    if not sendero:
        return Response({"detail": "El sendero no existe."}, status=400)

    RegistroVisita.objects.create(
        visitante=visitante,
        sendero_visitado=sendero.nombre_sendero,
        razon_visita=razon
    )

    return Response({"mensaje": "Visita registrada correctamente."}, status=201)


# ==============================
# Dashboard Endpoints
# ==============================

@api_view(['GET'])
def visitas_recientes(request):
    """
    Obtiene las visitas recientes con toda la información necesaria.
    Retorna: Fecha, Nombre, Adulto, Niño, Nacionalidad, Motivo de Visita, Sendero, Hora de Entrada, Teléfono
    """
    try:
        visitas = dashboard_service.obtener_visitas_recientes()
        return Response(visitas, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": "Error al obtener visitas recientes", "detalle": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def visitantes_hoy(request):
    """
    Retorna el conteo de visitantes de hoy.
    """
    try:
        count = dashboard_service.contar_visitantes_hoy()
        return Response({"visitantes_hoy": count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": "Error al contar visitantes de hoy", "detalle": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def encuestas_hoy(request):
    """
    Retorna el conteo de encuestas llenadas hoy.
    """
    try:
        count = dashboard_service.contar_encuestas_hoy()
        return Response({"encuestas_hoy": count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": "Error al contar encuestas de hoy", "detalle": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def visitantes_por_pais(request):
    """
    Retorna el conteo de visitantes agrupados por país/nacionalidad.
    """
    try:
        datos = dashboard_service.obtener_visitantes_por_pais()
        return Response(datos, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": "Error al obtener visitantes por país", "detalle": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def visitantes_por_sendero(request):
    """
    Retorna el conteo de visitantes agrupados por sendero.
    """
    try:
        datos = dashboard_service.obtener_visitantes_por_sendero()
        return Response(datos, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": "Error al obtener visitantes por sendero", "detalle": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def reporte_excel(request):
    """
    Genera y descarga el reporte completo en Excel.
    """
    try:
        # Generar el reporte
        excel_file = generar_reporte_completo()
        
        # Crear nombre del archivo con fecha y hora
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reporte_completo_centro_visitantes_{timestamp}.xlsx"
        
        # Crear respuesta HTTP para descarga
        response = HttpResponse(
            excel_file,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        # En caso de error, devolver JSON con el error
        return Response(
            {
                "error": "Error al generar el reporte completo",
                "detalle": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
