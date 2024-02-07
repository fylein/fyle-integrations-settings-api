from rest_framework import serializers

from apps.bamboohr.models import BambooHr, BambooHrConfiguration


class BambooHrSerializer(serializers.ModelSerializer):
    """
     Serializer for the Org API
    """
    class Meta:
        model = BambooHr
        fields = '__all__'


class BambooHrConfigurationSerializer(serializers.ModelSerializer):
    """
     Serializer For BamhooHrConfigurations
    """

    org = serializers.CharField()

    class Meta:
        model = BambooHrConfiguration
        fields = '__all__'
