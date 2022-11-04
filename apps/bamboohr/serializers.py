from rest_framework import serializers

from .models import BambooHr

class BambooHrSerializer(serializers.ModelSerializer):
    """
    BambooHr serializer
    """

    class Meta:
        model = BambooHr
        fields = '__all__'
