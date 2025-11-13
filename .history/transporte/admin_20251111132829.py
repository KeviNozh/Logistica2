from django.contrib import admin
from .models import *

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ['origen', 'destino', 'tipo_transporte', 'distancia_km']

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['patente', 'tipo_vehiculo', 'modelo', 'capacidad_kg', 'activo']

@admin.register(Aeronave)
class AeronaveAdmin(admin.ModelAdmin):
    list_display = ['matricula', 'tipo_aeronave', 'modelo', 'capacidad_kg', 'activo']

@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'licencia', 'activo']

@admin.register(Piloto)
class PilotoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'certificacion', 'horas_vuelo', 'activo']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['razon_social', 'rut', 'persona_contacto', 'activo']

@admin.register(Carga)
class CargaAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'tipo_carga', 'peso_kg', 'cliente']

@admin.register(Seguro)
class SeguroAdmin(admin.ModelAdmin):
    list_display = ['numero_poliza', 'tipo_seguro', 'aseguradora', 'estado']

@admin.register(Despacho)
class DespachoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ruta', 'estado', 'costo_envio', 'fecha_despacho']