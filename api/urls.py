from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VisitanteViewSet, 
    registro_usuario, obtener_usuario, 
    mostrar_sendero, listar_senderos, 
    mostrar_foto_sendero, listar_fotos_senderos,
    login_usuario,
    obtener_visitante_por_cedula, registrar_visita,
    visitas_recientes, visitantes_hoy, encuestas_hoy, visitantes_por_pais, visitantes_por_sendero, agregar_comentario,
    comentarios_por_sendero,
    valoracion_promedio,
    valoraciones_por_sendero,
    registrar_encuesta_view, 
)
from api import views

router = DefaultRouter()
router.register(r'visitantes', VisitanteViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Usuarios
    path('registro/', registro_usuario, name='registro-usuario'),
    path('usuario/<int:id>/', obtener_usuario, name='obtener-usuario'),
    path('login/', login_usuario, name='login-usuario'),

    # Senderos
    path('sendero/<int:id>/', mostrar_sendero, name='mostrar-sendero'),
    path('senderos/', listar_senderos, name='listar-senderos'),

    # Fotos de senderos
    path('foto-sendero/<int:id>/', mostrar_foto_sendero, name='mostrar-foto-sendero'),
    path('fotos-senderos/', listar_fotos_senderos, name='listar-fotos-senderos'),

    # Rutas para comentarios
    path('comentarios/agregar/', agregar_comentario, name='agregar-comentario'),
    path('comentarios/sendero/<int:sendero_id>/', comentarios_por_sendero, name='comentarios-por-sendero'),

    # Rutas para valoraciones
    path('valoracion-promedio/<int:sendero_id>/', valoracion_promedio, name='valoracion-promedio'),
    path('comentarios/<int:sendero_id>/valoraciones/', valoraciones_por_sendero, name='valoraciones-por-sendero'),
    
    # Visitantes
    path('visitante/cedula/<str:cedula>/', obtener_visitante_por_cedula, name='visitante-por-cedula'),

    # Registro de visita
    path('registrar_visitante_y_visita/', views.registrar_visitante_y_visita, name='registrar-visita-y-visitas'),
    path('registro-visita/', registrar_visita, name='registro-visita'),
    path('registrar-visita-id/', views.registrar_visita_por_id, name='registrar-visita-id'),

    # Dashboard endpoints
    path('dashboard/visitas-recientes/', visitas_recientes, name='visitas-recientes'),
    path('dashboard/visitantes-hoy/', visitantes_hoy, name='visitantes-hoy'),
    path('dashboard/encuestas-hoy/', encuestas_hoy, name='encuestas-hoy'),
    path('dashboard/visitantes-por-pais/', visitantes_por_pais, name='visitantes-por-pais'),
    path('dashboard/visitantes-por-sendero/', visitantes_por_sendero, name='visitantes-por-sendero'),

    # Encuesta
    path('encuestas/registrar/', registrar_encuesta_view),
]