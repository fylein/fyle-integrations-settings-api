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

    def create(self, validated_data):        
        org = validated_data['org']
        
        configuration, _ = BambooHrConfiguration.objects.update_or_create(
            org_id=org,
            defaults={
                'recipe_status': True,
                'additional_email_options': validated_data['additional_email_options'],
                'emails_selected': validated_data['emails_selected']
            }
        )

        return configuration

    class Meta:
        model = BambooHrConfiguration
        fields = '__all__'
        read_only_fields = [
            'recipe_id'
        ]
