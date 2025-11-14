from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'transporte/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    context = {
        'total_despachos': Despacho.objects.count(),
        'despachos_pendientes': Despacho.objects.filter(estado='PENDIENTE').count(),
        'total_vehiculos': Vehiculo.objects.filter(activo=True).count(),
        'total_clientes': Cliente.objects.filter(activo=True).count(),
    }
    return render(request, 'transporte/dashboard.html', context)

@login_required
def despachos_view(request):
    despachos = Despacho.objects.all().order_by('-fecha_despacho')
    return render(request, 'transporte/despachos.html', {'despachos': despachos})

@login_required
def rutas_view(request):
    rutas = Ruta.objects.all()
    return render(request, 'transporte/rutas.html', {'rutas': rutas})

@login_required
def vehiculos_view(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'transporte/vehiculos.html', {'vehiculos': vehiculos})

@login_required
def aeronaves_view(request):
    aeronaves = Aeronave.objects.all()
    return render(request, 'transporte/aeronaves.html', {'aeronaves': aeronaves})

@login_required
def conductores_view(request):
    conductores = Conductor.objects.all()
    return render(request, 'transporte/conductores.html', {'conductores': conductores})

@login_required
def pilotos_view(request):
    pilotos = Piloto.objects.all()
    return render(request, 'transporte/pilotos.html', {'pilotos': pilotos})

@login_required
def clientes_view(request):
    clientes = Cliente.objects.all()
    return render(request, 'transporte/clientes.html', {'clientes': clientes})

@login_required
def cargas_view(request):
    cargas = Carga.objects.all()
    return render(request, 'transporte/cargas.html', {'cargas': cargas})

@login_required
def seguros_view(request):
    seguros = Seguro.objects.all()
    return render(request, 'transporte/seguros.html', {'seguros': seguros})

@login_required
def reportes_view(request):
    return render(request, 'transporte/reportes.html')

@login_required
def api_view(request):
    return render(request, 'transporte/api.html')