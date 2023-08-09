from apps.orgs.actions import post_package
from apps.orgs.models import Org
from apps.travelperk.models import TravelPerk, TravelPerkConfiguration
from workato import Workato



def get_all_managed_user():
    org_ids = Org.objects.values_list('id', flat=True)
    return org_ids

def post_package_to_workato():
    connector = Workato()
    org_ids = get_all_managed_user()
    count=0
    for org_id in org_ids:
        org = Org.objects.get(id=org_id)
        managed_user=None
        if org.managed_user_id:
            try:
                managed_user = connector.managed_users.get_by_id(org.fyle_org_id)
            except:
                print("managed user not found")
            if managed_user:
                travelperk = TravelPerk.objects.filter(org_id = org_id).first()
                if travelperk:
                    travelperk_conf = TravelPerkConfiguration.objects.filter(org_id=org_id).first()
                    if travelperk_conf and travelperk_conf.is_recipe_enabled:
                        try:
                            connector.recipes.post(org.managed_user_id, travelperk_conf.recipe_id, None, 'stop')
                        except:
                            print('no recipe found')
                    try:
                        package = post_package(
                            org_id=org_id,
                            folder_id=travelperk.folder_id,
                            package_path='assets/travelperk.zip'
                        )
                        travelperk.package_id = package['id']
                        travelperk.save()
                    except:
                        print('error uploading package to workato')
                    if travelperk_conf and travelperk_conf.is_recipe_enabled:
                        try:
                            connector.recipes.post(org.managed_user_id, travelperk_conf.recipe_id, None, 'start')
                        except:
                            print('error while starting the recipe')
                    count +=1
                    print(org.name,count)

