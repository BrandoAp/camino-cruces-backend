from ..models import Comentario
from ..serializers import ComentarioSerializer


def crear_comentario(data):
    serializer = ComentarioSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    comentario = serializer.save()
    return comentario


def listar_comentarios_por_sendero(sendero_id):
    return Comentario.objects.filter(sendero_id=sendero_id)

