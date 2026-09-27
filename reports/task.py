from celery import shared_task
from .models import Report
import time

@shared_task
def generate_report(report_id):
    try:
        report = Report.objects.get(id=report_id)
        
        report.status = 'processing'
        
        report.save()
        
        time.sleep(5)
        
        report.result = f"Repoerte generado:{report.title}"
        
        report.status = 'completed'
        
        report.save()
        
        return f"Repoerte {report_id} completado"
    
    except Report.DoesNotExist:
        return f"Reporte {report_id} no encontrado"
    
    except Exception as e:
        report.status = 'failed'
        report.result = str(e)
        report.save()
        return f"Error: {str(e)}"
    
    