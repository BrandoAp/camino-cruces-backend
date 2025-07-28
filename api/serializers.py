from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (
    Visitante, Sendero, SenderoFoto,
    RegistroVisita, Encuesta,
    Usuario, Comentario
)


class VisitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitante
        fields = '__all__'


class SenderoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sendero
        fields = '__all__'


class SenderoFotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenderoFoto
        fields = '__all__'


class RegistroVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroVisita
        fields = '__all__'


class EncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.ChoiceField(choices=Usuario.Rol.choices, default=Usuario.Rol.USER)
    contraseña = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'apellido', 'contraseña', 'rol']

    def create(self, validated_data):
        contraseña = validated_data.pop('contraseña', None)
        instance = Usuario(**validated_data)
        if contraseña is not None:
            instance.contraseña = make_password(contraseña)
        instance.save()
        return instance



class ComentarioSerializer(serializers.ModelSerializer):
    usuario_id = serializers.PrimaryKeyRelatedField(
        source='usuario',
        queryset=Usuario.objects.all(),
        write_only=True
    )
    usuario = serializers.StringRelatedField(read_only=True)  # Mostrar el usuario como string
    sendero = serializers.PrimaryKeyRelatedField(queryset=Sendero.objects.all())
    foto_comentario = serializers.URLField(required=False, allow_null=True)


    class Meta:
        model = Comentario
        fields = ['usuario_id', 'usuario', 'sendero', 'foto_comentario', 'comentario', 'valoracion']

    def validate_valoracion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La valoración debe estar entre 1 y 5.")
        return value
