from rest_framework import viewsets
from .models import *
from .serializers import *

# Vistas para API
class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class AeronaveViewSet(viewsets.ModelViewSet):
    queryset = Aeronave.objects.all()
    serializer_class = AeronaveSerializer

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer

class PilotoViewSet(viewsets.ModelViewSet):
    queryset = Piloto.objects.all()
    serializer_class = PilotoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class CargaViewSet(viewsets.ModelViewSet):
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer

class SeguroViewSet(viewsets.ModelViewSet):
    queryset = Seguro.objects.all()
    serializer_class = SeguroSerializer

class DespachoViewSet(viewsets.ModelViewSet):
    queryset = Despacho.objects.all()
    serializer_class = DespachoSerializer

# Vistas para templates HTML
from django.shortcuts import render

def dashboard(request):
    return render(request, 'transporte/dashboard.html')

def despachos_view(request):
    return render(request, 'transporte/despachos.html')

def rutas_view(request):
    return render(request, 'transporte/rutas.html')

def vehiculos_view(request):
    return render(request, 'transporte/vehiculos.html')

def aeronaves_view(request):
    return render(request, 'transporte/aeronaves.html')

def conductores_view(request):
    return render(request, 'transporte/conductores.html')

def pilotos_view(request):
    return render(request, 'transporte/pilotos.html')

def clientes_view(request):
    return render(request, 'transporte/clientes.html')

def cargas_view(request):
    return render(request, 'transporte/cargas.html')

def seguros_view(request):
    return render(request, 'transporte/seguros.html')

def reportes_view(request):
    return render(request, 'transporte/reportes.html')

def api_view(request):
    return render(request, 'transporte/api.html')