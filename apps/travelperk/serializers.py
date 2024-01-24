from rest_framework import serializers

from workato import Workato
from apps.travelperk.models import TravelPerk, TravelPerkConfiguration, InvoiceLineItem, TravelperkAdvancedSetting
from apps.travelperk.connector import TravelperkConnector
from apps.orgs.models import Org
from apps.travelperk.models import (
    TravelPerk, 
    TravelPerkConfiguration, 
    InvoiceLineItem, 
    TravelperkProfileMapping, 
    TravelperkCredential
)


class TravelperkSerializer(serializers.ModelSerializer):
    """
    Serializer for the Travelperk API
    """
    class Meta:
        model = TravelPerk
        fields = '__all__'


class TravelPerkConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer For Travelperk Configurations
    """

    org = serializers.CharField()

    def create(self, validated_data):        
        org = validated_data['org']
        connector = Workato()
        managed_user_id = Org.objects.get(id=org).managed_user_id
        recipes = connector.recipes.get(managed_user_id)['result']

        travelperk_configuration, _ = TravelPerkConfiguration.objects.update_or_create(
            defaults={
                'org_id':org,
                'recipe_id':recipes[0]['id'],
                'recipe_data': recipes[0]['code'],
                'is_recipe_enabled': True
            }
        )

        connector.recipes.post(managed_user_id, travelperk_configuration.recipe_id, None, 'start')

        return travelperk_configuration

    class Meta:
        model = TravelPerkConfiguration
        fields = '__all__'
        read_only_fields = [
            'recipe_id'
        ]


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = '__all__'


class TravelperkAdvancedSettingSerializer(serializers.ModelSerializer):
    """
    Serializer for Travelperk Advanced Settings
    """

    class Meta:
        model = TravelperkAdvancedSetting
        fields = '__all__'

    def create(self, validated_data):
        """
        Create Advanced Settings
        """
        org_id = self.context['request'].parser_context.get('kwargs').get('org_id')
        advanced_setting = TravelperkAdvancedSetting.objects.filter(
            org_id=org_id
        ).first()

        if not advanced_setting:
            if 'description_structure' not in validated_data:
                validated_data['description_structure'] = [
                    'trip_id',
                    'trip_name',
                    'traveller_name',
                    'merchant_name',
                    'booker_name',
                ]

        advanced_setting, _ = TravelperkAdvancedSetting.objects.update_or_create(
            org_id=org_id,
            defaults=validated_data
        )
class TravelperkProfileMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelperkProfileMapping
        fields = '__all__'

    def create(self, validated_data):
        
        org_id = self.context['request'].parser_context.get('kwargs').get('org_id')
        travelperk_profile_mapping, _ = TravelperkProfileMapping.objects.update_or_create(
            org_id=org_id,
            profile_name=validated_data['profile_name'],
            defaults=validated_data
        )

        return travelperk_profile_mapping


class SyncPaymentProfileSerializer(serializers.Serializer):
    """
    Serializer for Sync Payment Profile
    """

    def sync_payment_profiles(self, org_id):
        """
        Sync Payment Profile
        """

        travelperk_credentials = TravelperkCredential.objects.get(org_id=org_id)

        travelperk_connection = TravelperkConnector(travelperk_credentials, org_id)
        travelperk_connection.sync_invoice_profile()
