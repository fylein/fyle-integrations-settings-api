import json
from rest_framework import serializers
from django.conf import settings

from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.orgs.models import Org
from workato import Workato


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
