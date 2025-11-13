from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

# Vistas basadas en clases para templates HTML
class RutaListView(LoginRequiredMixin, ListView):
    model = Ruta
    template_name = 'transporte/rutas.html'
    context_object_name = 'rutas'

class RutaDetailView(LoginRequiredMixin, DetailView):
    model = Ruta
    template_name = 'transporte/ruta_detail.html'

class RutaCreateView(LoginRequiredMixin, CreateView):
    model = Ruta
    template_name = 'transporte/ruta_form.html'
    fields = ['origen', 'destino', 'tipo_transporte', 'distancia_km']
    success_url = reverse_lazy('rutas')

class RutaUpdateView(LoginRequiredMixin, UpdateView):
    model = Ruta
    template_name = 'transporte/ruta_form.html'
    fields = ['origen', 'destino', 'tipo_transporte', 'distancia_km']
    success_url = reverse_lazy('rutas')

class RutaDeleteView(LoginRequiredMixin, DeleteView):
    model = Ruta
    template_name = 'transporte/ruta_confirm_delete.html'
    success_url = reverse_lazy('rutas')

# Vistas de autenticación
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'transporte/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Validaciones
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'transporte/login.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return render(request, 'transporte/login.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'transporte/login.html')
        
        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            
            # Autenticar y loguear al usuario
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido {user.first_name}')
                return redirect('dashboard')
                
        except Exception as e:
            messages.error(request, 'Error al crear la cuenta')
    
    return render(request, 'transporte/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('login')

# Vistas para templates HTML (funciones)
@login_required
def dashboard(request):
    # Estadísticas para el dashboard
    total_despachos = Despacho.objects.count()
    despachos_pendientes = Despacho.objects.filter(estado='PENDIENTE').count()
    despachos_en_ruta = Despacho.objects.filter(estado='EN_RUTA').count()
    total_vehiculos = Vehiculo.objects.filter(activo=True).count()
    total_aeronaves = Aeronave.objects.filter(activo=True).count()
    
    context = {
        'total_despachos': total_despachos,
        'despachos_pendientes': despachos_pendientes,
        'despachos_en_ruta': despachos_en_ruta,
        'total_vehiculos': total_vehiculos,
        'total_aeronaves': total_aeronaves,
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
    # Datos para reportes
    despachos_por_estado = Despacho.objects.values('estado').annotate(total=models.Count('id'))
    cargas_por_tipo = Carga.objects.values('tipo_carga').annotate(total=models.Count('id'))
    
    context = {
        'despachos_por_estado': despachos_por_estado,
        'cargas_por_tipo': cargas_por_tipo,
    }
    return render(request, 'transporte/reportes.html', context)

@login_required
def api_view(request):
    return render(request, 'transporte/api.html')

# Vistas para crear/editar/eliminar (funciones básicas)
@login_required
def crear_despacho(request):
    if request.method == 'POST':
        # Lógica para crear despacho
        messages.success(request, 'Despacho creado exitosamente')
        return redirect('despachos')
    return render(request, 'transporte/despacho_form.html')

@login_required
def editar_despacho(request, pk):
    despacho = get_object_or_404(Despacho, pk=pk)
    if request.method == 'POST':
        # Lógica para editar despacho
        messages.success(request, 'Despacho actualizado exitosamente')
        return redirect('despachos')
    return render(request, 'transporte/despacho_form.html', {'despacho': despacho})