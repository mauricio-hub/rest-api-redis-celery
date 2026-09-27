from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Report
from .serializers import ReportSerializer
from .task import generate_report

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
    def create(self, request, *args, **kwargs):
        """Override para crear reporte y enviar a cola"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Guardar el reporte
        report = serializer.save()
        
        generate_report.delay(report.id)
         
        # Aqui enviaremos a Celery (por ahora solo creamos)
        
        return Response(serializer.data, status=201)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Endpoint para ver el status del reporte"""
        report = self.get_object()
        return Response({
            'id': report.id,
            'title': report.title,
            'status': report.status,
            'result': report.result
        })