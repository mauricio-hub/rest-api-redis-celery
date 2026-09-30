from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Report
from .serializers import ReportSerializer
from .task import generate_report
from celery.result import AsyncResult


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
    def create(self, request, *args, **kwargs):
        """Override para crear reporte y enviar a cola"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Guardar el reporte
        report = serializer.save()
        
        task = generate_report.delay(report.id)
        
        report.task_id = task.id
        
        report.save() 
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
        
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Endpoint para ver el status del reporte"""
        print("PROGRESS CALLED")
        
        report = self.get_object()
        print(f"Report ID: {report.id}")
        print(f"Report task_id: {report.task_id}")
        
        if not report.task_id:
            print("task_id is None or empty")
            return Response({
                'error': 'No task_id found',
                'status': report.status
            })
        
        print(f"task_id found: {report.task_id}")
        
        task_id = report.task_id
        task_result = AsyncResult(task_id)
        
        print(f"🔍 AsyncResult state: {task_result.state}")
        print(f"🔍 AsyncResult result: {task_result.result}")
        print(f"🔍 AsyncResult id: {task_result.id}")
        
        return Response({
            'task_id': task_result.id,
            'state': task_result.state,
            'result': task_result.result,
            'status': report.status
        })