import json
from rest_framework import serializers

from apps.gusto.models import Gusto, GustoConfiguration
from apps.orgs.models import Org
from workato import Workato


class GustoSerializer(serializers.ModelSerializer):
    """
     Serializer for the Org API
    """
    class Meta:
        model = Gusto
        fields = '__all__'


class GustoConfigurationSerializer(serializers.ModelSerializer):
    """
     Serializer For GustoConfigurations
    """

    org = serializers.CharField()

    def create(self, validated_data):        
        org = validated_data['org']
        connector = Workato()
        managed_user_id = Org.objects.get(id=org).managed_user_id
        recipes = connector.recipes.get(managed_user_id)['result']

        configuration, _ = GustoConfiguration.objects.update_or_create(
            defaults={
                'org_id': org,
                'recipe_id': recipes[0]['id'],
                'recipe_status': True,
                'recipe_data': recipes[0]['code'],
                'additional_email_options': validated_data['additional_email_options'],
                'emails_selected': validated_data['emails_selected']
            }
        )

        connector.recipes.post(managed_user_id, configuration.recipe_id, None, 'start')

        return configuration

    class Meta:
        model = GustoConfiguration
        fields = '__all__'
        read_only_fields = [
            'recipe_id'
        ]
