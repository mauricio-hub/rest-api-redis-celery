from celery import shared_task
from .models import Report
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
@shared_task(bind=True, autoretry_for=(Exception,),retry_kwargs={'max_retries':3})
def generate_report(self , report_id):
    try:
        report = Report.objects.get(id=report_id)
        
        report.status = 'processing'
        
        report.save()
        
        time.sleep(5)
        # Crear carpeta si no existe
        os.makedirs("media/reports/", exist_ok=True)
        report.result = f"Reporte generado:{report.title}"
        
        # import the canvas object
    

        # create a Canvas object with a filename
        
        pdf_path = f"media/reports/report_{report_id}.pdf"
        
        c = canvas.Canvas(pdf_path, pagesize=(595.27, 841.89))  # A4 pagesize

        c.drawString(50, 780, f"Report: {report.title}")
        # finish page
        c.showPage()
        # construct and save file to .pdf
       # print('aqui va ...',c)
        c.save()
        
        report.status = 'completed'
        
        report.save()
        
        return f"Reporte {report_id} completado"
    
    except Report.DoesNotExist:
        return f"Reporte {report_id} no encontrado"
    
    except Exception as e:
        report.status = 'failed'
        report.result = str(e)
        report.save()
        return f"Error: {str(e)}"
    
    