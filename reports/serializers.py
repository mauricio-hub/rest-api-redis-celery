from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'title', 'status', 'created_at', 'updated_at', 'result']
        read_only_fields = ['id', 'created_at', 'updated_at', 'status', 'result']