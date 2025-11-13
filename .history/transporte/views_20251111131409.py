from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import *
from .serializers import *
from .permissions import *

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_transporte']
    search_fields = ['origen', 'destino']
    ordering_fields = ['distancia_km']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_vehiculo', 'activo']
    search_fields = ['patente', 'modelo']
    ordering_fields = ['capacidad_kg', 'año']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class AeronaveViewSet(viewsets.ModelViewSet):
    queryset = Aeronave.objects.all()
    serializer_class = AeronaveSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_aeronave', 'activo']
    search_fields = ['matricula', 'modelo']
    ordering_fields = ['capacidad_kg']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activo']
    search_fields = ['nombre', 'rut', 'licencia']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class PilotoViewSet(viewsets.ModelViewSet):
    queryset = Piloto.objects.all()
    serializer_class = PilotoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activo']
    search_fields = ['nombre', 'rut', 'certificacion']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_cliente', 'activo']
    search_fields = ['razon_social', 'persona_contacto', 'rut']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class CargaViewSet(viewsets.ModelViewSet):
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_carga', 'cliente']
    search_fields = ['descripcion']
    ordering_fields = ['peso_kg', 'valor_declarado']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class SeguroViewSet(viewsets.ModelViewSet):
    queryset = Seguro.objects.all()
    serializer_class = SeguroSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_seguro', 'estado', 'aseguradora']
    search_fields = ['numero_poliza']
    ordering_fields = ['cobertura', 'vigencia_hasta']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def por_vencer(self, request):
        from datetime import date, timedelta
        fecha_limite = date.today() + timedelta(days=30)
        seguros = Seguro.objects.filter(
            vigencia_hasta__lte=fecha_limite,
            vigencia_hasta__gte=date.today()
        )
        serializer = self.get_serializer(seguros, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def vencidos(self, request):
        from datetime import date
        seguros = Seguro.objects.filter(vigencia_hasta__lt=date.today())
        serializer = self.get_serializer(seguros, many=True)
        return Response(serializer.data)

class DespachoViewSet(viewsets.ModelViewSet):
    queryset = Despacho.objects.all()
    serializer_class = DespachoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'ruta__tipo_transporte', 'cliente']
    search_fields = ['ruta__origen', 'ruta__destino', 'cliente__razon_social']
    ordering_fields = ['fecha_despacho', 'costo_envio']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        despacho = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in dict(EstadoDespacho.choices):
            return Response(
                {'error': 'Estado no válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        despacho.estado = nuevo_estado
        despacho.save()
        
        serializer = self.get_serializer(despacho)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        from django.db.models import Count, Sum, Avg
        from datetime import date, timedelta
        
        # Estadísticas generales
        total_despachos = Despacho.objects.count()
        despachos_activos = Despacho.objects.filter(estado='EN_RUTA').count()
        despachos_completados = Despacho.objects.filter(estado='ENTREGADO').count()
        
        # Ingresos del mes
        inicio_mes = date.today().replace(day=1)
        ingresos_mes = Despacho.objects.filter(
            fecha_despacho__gte=inicio_mes,
            estado='ENTREGADO'
        ).aggregate(total=Sum('costo_envio'))['total'] or 0
        
        # Despachos por tipo de transporte
        por_tipo = Despacho.objects.values('ruta__tipo_transporte').annotate(
            total=Count('id')
        )
        
        return Response({
            'total_despachos': total_despachos,
            'despachos_activos': despachos_activos,
            'despachos_completados': despachos_completados,
            'ingresos_mes': float(ingresos_mes),
            'despachos_por_tipo': list(por_tipo)
        })

# Vista para dashboard
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'transporte/dashboard.html')

@login_required
def despachos_view(request):
    return render(request, 'transporte/despachos.html')

@login_required
def vehiculos_view(request):
    return render(request, 'transporte/vehiculos.html')

@login_required
def aeronaves_view(request):
    return render(request, 'transporte/aeronaves.html')

@login_required
def conductores_view(request):
    return render(request, 'transporte/conductores.html')

@login_required
def pilotos_view(request):
    return render(request, 'transporte/pilotos.html')

@login_required
def clientes_view(request):
    return render(request, 'transporte/clientes.html')

@login_required
def cargas_view(request):
    return render(request, 'transporte/cargas.html')

@login_required
def seguros_view(request):
    return render(request, 'transporte/seguros.html')

@login_required
def reportes_view(request):
    return render(request, 'transporte/reportes.html')

@login_required
def api_view(request):
    return render(request, 'transporte/api.html')