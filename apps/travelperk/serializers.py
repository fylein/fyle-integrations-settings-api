from rest_framework import serializers

from apps.travelperk.actions import add_travelperk_to_integrations
from apps.travelperk.models import TravelPerk, InvoiceLineItem
from apps.travelperk.connector import TravelperkConnector
from apps.travelperk.models import (
    TravelPerk, 
    InvoiceLineItem, 
    TravelperkProfileMapping, 
    TravelperkCredential,
    TravelperkAdvancedSetting
)


class TravelperkSerializer(serializers.ModelSerializer):
    """
    Serializer for the Travelperk API
    """
    class Meta:
        model = TravelPerk
        fields = '__all__'


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
        fields = [
            'default_employee_name',
            'default_employee_id',
            'default_category_name',
            'default_category_id',
            'invoice_lineitem_structure',
            'description_structure',
            'category_mappings',
            'org'
        ]
        read_only_fields = ('id', 'org', 'created_at', 'updated_at')


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
        
        travelperk = TravelPerk.objects.filter(org_id=org_id).first()
        if travelperk.onboarding_state == 'ADVANCED_SETTINGS':
            travelperk.onboarding_state = 'COMPLETE'
            travelperk.save()
            add_travelperk_to_integrations(org_id)

        return advanced_setting


class TravelperkProfileMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelperkProfileMapping
        fields = '__all__'


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
        payment_profiles = travelperk_connection.sync_invoice_profile()
        return payment_profiles
