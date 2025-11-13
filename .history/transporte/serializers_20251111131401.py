from rest_framework import serializers
from .models import *

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    conductor_nombre = serializers.CharField(source='conductor_asignado.nombre', read_only=True)
    
    class Meta:
        model = Vehiculo
        fields = '__all__'

class AeronaveSerializer(serializers.ModelSerializer):
    piloto_nombre = serializers.CharField(source='piloto_asignado.nombre', read_only=True)
    
    class Meta:
        model = Aeronave
        fields = '__all__'

class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = '__all__'

class PilotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piloto
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CargaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.razon_social', read_only=True)
    
    class Meta:
        model = Carga
        fields = '__all__'

class SeguroSerializer(serializers.ModelSerializer):
    asegurado = serializers.SerializerMethodField()
    
    class Meta:
        model = Seguro
        fields = '__all__'
    
    def get_asegurado(self, obj):
        if obj.vehiculo:
            return f"{obj.vehiculo.patente} (Vehículo)"
        elif obj.aeronave:
            return f"{obj.aeronave.matricula} (Aeronave)"
        elif obj.carga:
            return f"{obj.carga.descripcion} (Carga)"
        return "No especificado"

class DespachoSerializer(serializers.ModelSerializer):
    ruta_info = serializers.CharField(source='ruta.__str__', read_only=True)
    vehiculo_info = serializers.CharField(source='vehiculo.__str__', read_only=True)
    aeronave_info = serializers.CharField(source='aeronave.__str__', read_only=True)
    conductor_info = serializers.CharField(source='conductor.__str__', read_only=True)
    piloto_info = serializers.CharField(source='piloto.__str__', read_only=True)
    cliente_info = serializers.CharField(source='cliente.__str__', read_only=True)
    carga_info = serializers.CharField(source='carga.__str__', read_only=True)
    
    class Meta:
        model = Despacho
        fields = '__all__'