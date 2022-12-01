from rest_framework import serializers
from apps.bamboohr.models import BambooHr, Configuration

class BambooHrSerializer(serializers.ModelSerializer):
    """
     Serializer for the Org API
    """
    class Meta:
        model = BambooHr
        fields = '__all__'


class ConfigurationSerializer(serializers.ModelSerializer):
    """
     Serializer For Configurations
    """
    class Meta:
        model = Configuration
        fields = '__all__'
        read_only_fields = [
            'org', 'recipe_id', 'start_datetime', 'interval_hours',
            'emails_selected', 'additional_email_options'
        ]

    def update(self, instance, validated):
        auth = self.context['request'].META.get('HTTP_AUTHORIZATION')
        access_token = auth.split(' ')[1]
        
        print('auth', auth)

        return access_token
