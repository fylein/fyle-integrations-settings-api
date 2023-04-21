from rest_framework import serializers

from workato import Workato
from apps.travelperk.models import TravelPerk, TravelPerkConfiguration
from apps.orgs.models import Org


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
