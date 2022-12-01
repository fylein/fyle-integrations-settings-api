from rest_framework import serializers
from apps.bamboohr.models import BambooHr

class BambooHrSerializer(serializers.ModelSerializer):
    """
     Serializer for the Org API
    """
    class Meta:
        model = BambooHr
        fields = '__all__'
