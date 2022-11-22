"""
Orgs Serializers
"""
import logging
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.orgs.models import FyleCredential, Org

from fyle_rest_auth.models import AuthToken
from fyle_rest_auth.helpers import get_fyle_admin
from apps.users.helpers import get_cluster_domain
from apps.orgs.models import FyleCredential, Org, User

User = get_user_model()

logger = logging.getLogger(__name__)
logger.level = logging.INFO

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
        read_only_fields = [
            'name', 'fyle_org_id', 'cluster_domain', 'user'
        ]

    def update(self, instance, validated):
        
        auth = self.context['request'].META.get('HTTP_AUTHORIZATION')
        access_token = auth.split(' ')[1]

        fyle_user = get_fyle_admin(access_token, None)

        org_name = fyle_user['data']['org']['name']
        org_id = fyle_user['data']['org']['id']
        org = Org.objects.filter(fyle_org_id=org_id).first()

        if org:
            org.user.add(User.objects.get(user_id=self.context['request'].user))
        else:
            auth_tokens = AuthToken.objects.get(user__user_id=self.context['request'].user)
            cluster_domain = get_cluster_domain(auth_tokens.refresh_token)
            org = Org.objects.create(name=org_name, fyle_org_id=org_id, cluster_domain=cluster_domain)
            org.user.add(User.objects.get(user_id=self.context['request'].user))

            FyleCredential.objects.update_or_create(
                refresh_token=auth_tokens.refresh_token,
                org_id=org.id
            )

        return org
