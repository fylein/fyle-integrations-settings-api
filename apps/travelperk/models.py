from django.db import models

from apps.orgs.models import Org

# Create your models here.
class TravelPerk(models.Model):
    """
    Travelperk Model
    """
    
    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Org')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org table')
    folder_id = models.CharField(max_length=255, null=True, help_text='Travelperk Folder ID')
    package_id = models.CharField(max_length=255, null=True, help_text="Travelperk Package ID")
    is_s3_connected = models.BooleanField(null=True, help_text='If S3 Is Connectoed')
    is_travel_perk_connected = models.BooleanField(null=True, help_text='If Travelperk Is Connected')
    travelperk_connection_id = models.IntegerField(null=True, help_text='Travelperk Connection Id')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at =  models.DateTimeField(auto_now=True, help_text='Updated at datetime')

    class Meta:
       db_table = 'travelperk'


class TravelPerkConfiguration(models.Model):
    """
    TravelperkConfiguration Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Configuration')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org Table')
    recipe_id = models.CharField(max_length=255, help_text='Recipe Id', null=True)
    recipe_data = models.TextField(help_text='Code For Recipe', null=True)
    is_recipe_enabled = models.BooleanField(help_text='recipe status', null=True)

    class Meta:
        db_table = 'travelperk_configurations'