from rest_framework import serializers
from .models import ProjectInquiry


class ProjectInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInquiry
        fields = "__all__"