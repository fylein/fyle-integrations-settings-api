from datetime import datetime
from rest_framework import serializers

from apps.integrations.models import Integration


class IntegrationSerializer(serializers.ModelSerializer):
    """
     Serializer for the Integrations API
    """
    org_id = serializers.CharField(read_only=True)
    org_name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Create or Update Integration
        :param validated_data: Validated data
        :return: upserted integrations object
        """

        if validated_data['is_active']:
            integration, _ = Integration.objects.update_or_create(
                org_id=validated_data['org_id'],
                type=validated_data['type'],
                defaults={
                    'is_active': True,
                    'org_name': validated_data['org_name'],
                    'tpa_id': validated_data['tpa_id'],
                    'tpa_name': validated_data['tpa_name'],
                    'errors_count': 0,
                    'unmapped_card_count': 0,
                    'unmapped_employee_count': 0,
                    'is_token_expired': False,
                    'has_payment_mode_changed': False
                }
            )
        elif not validated_data['is_active']:
            integration = Integration.objects.filter(org_id=validated_data['org_id'], type=validated_data['type']).first()

            integration.is_active=False
            integration.disconnected_at=datetime.now()
            integration.save()

        return integration

    class Meta:
        model = Integration
        fields = '__all__'
