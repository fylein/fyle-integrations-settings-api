"""
Orgs Serializers
"""
from rest_framework import serializers

from apps.orgs.models import FyleCredential, Org


class FyleCredentialSerializer(serializers.ModelSerializer):
    """
    Fyle credential serializer
    """
    class Meta:
        model = FyleCredential
        fields = '__all__'


class OrgSerializer(serializers.ModelSerializer):
    """
     Serializer for the Org API
    """
    class Meta:
        model = Org
        fields = '__all__'

