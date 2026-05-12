from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer with common read-only fields.
    """

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        abstract = True