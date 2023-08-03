from apps.orgs.actions import post_package
from apps.orgs.models import Org
from apps.travelperk.models import TravelPerk, TravelPerkConfiguration
from workato import Workato



def get_all_managed_user():
    org_ids = Org.objects.values_list('id', flat=True)
    return org_ids


def post_package_to_workato():
    connector = Workato()
    print("connected to worakto")
    org_ids = get_all_managed_user()
    count=0
    print("org_ids")
    for org_id in org_ids:
        org = Org.objects.get(id=org_id)
        if org.managed_user_id:
            print("inside if")
            travelperk = TravelPerk.objects.filter(org_id = org_id).first()
            if travelperk:
                travelperk_conf = TravelPerkConfiguration.objects.filter(org_id=org_id).first()
                print("inside travelperk")
                if travelperk_conf.is_recipe_enabled: 
                    print("inside travelperk_conf")
                    connector.recipes.post(org.managed_user_id, travelperk_conf.recipe_id, None, 'stop')
                    print("recipe stopped")
                    package = post_package(
                    org_id=org_id,
                    folder_id=travelperk.folder_id,
                    package_path='src/assets/travelperk.zip'
                    )
                    print("package posted")
                    print(package["id"])
                    travelperk.package_id = package['id']
                    travelperk.save()
                            
                    connector.recipes.post(org.managed_user_id, travelperk_conf.recipe_id, None, 'start')
                    print("recipe started")
                    count +=1						
                    print(org.name,count)
                    return "Success"
    return "No Orgs Found"

print(post_package_to_workato())