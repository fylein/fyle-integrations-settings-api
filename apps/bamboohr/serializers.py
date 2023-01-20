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
        connector = Workato()
        managed_user_id = Org.objects.get(id=org).managed_user_id
        recipes = connector.recipes.get(managed_user_id)['result']
        code = json.loads(recipes[0]['code'])

        admin_emails = [
            {
             'email': admin['email'],
            } for admin in validated_data['emails_selected']
        ]

        code['block'][0]['block'][2]['block'][0]['input']['personalizations'][0]['to'] = admin_emails
        code['block'][0]['block'][2]['block'][0]['input']['from']['email'] = settings.SENDGRID_EMAIL

        recipes[0]['code'] = json.dumps(code)

        payload = {
            "recipe": {
                "name": recipes[0]['name'],
                "code": recipes[0]['code'],
                "folder_id": str(recipes[0]['folder_id'])
            }
        }
        configuration, _ = BambooHrConfiguration.objects.update_or_create(
            org_id=org,
            recipe_id=recipes[0]['id'],
            defaults={
                'recipe_status': True,
                'recipe_data': recipes[0]['code'],
                'additional_email_options': validated_data['additional_email_options'],
                'emails_selected': validated_data['emails_selected']
            }
        )

        connector.recipes.post(managed_user_id, configuration.recipe_id, payload)
        connector.recipes.post(managed_user_id, configuration.recipe_id, None, 'start')

        return configuration

    class Meta:
        model = BambooHrConfiguration
        fields = '__all__'
        read_only_fields = [
            'recipe_id'
        ]
