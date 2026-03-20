from rest_framework import serializers
from .models import InternshipApplication

class InternshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipApplication
        fields = '__all__'
        read_only_fields = ['created_at', 'status']

    def validate(self, data):
        email = data.get('email')
        internship_type = data.get('internship_type')

        if InternshipApplication.objects.filter(
            email=email,
            internship_type=internship_type
        ).exists():
            raise serializers.ValidationError(
                "You have already applied for this internship."
            )

        return data