from rest_framework import serializers

from apps.travelperk.connector import TravelperkConnector
from apps.orgs.models import Org
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
