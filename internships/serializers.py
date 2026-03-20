from rest_framework import serializers
from .models import InternshipApplication


class InternshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipApplication
        fields = '__all__'
        read_only_fields = ['created_at', 'status']