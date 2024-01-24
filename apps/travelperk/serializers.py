from rest_framework import serializers

from apps.travelperk.models import TravelPerk, TravelPerkConfiguration, InvoiceLineItem
from apps.orgs.models import Org


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
