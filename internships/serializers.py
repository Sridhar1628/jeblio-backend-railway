from rest_framework import serializers
from .models import InternshipApplication


class InternshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipApplication
        fields = '__all__'