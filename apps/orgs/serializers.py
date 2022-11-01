"""
Orgs Serializers
"""
from rest_framework import serializers

from .models import Org, FyleCredential


class OrgSerializer(serializers.ModelSerializer):
    """
    Org serializer
    """

    class Meta:
        model = Org
        fields = '__all__'


class FyleCredentialSerializer(serializers.ModelSerializer):
    """
    Fyle credential serializer
    """

    class Meta:
        model = FyleCredential
        fields = '__all__'

