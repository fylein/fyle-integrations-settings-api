rollback;
begin;

with orgs as (
    select o.name, i.org_id as common_org_id from integrations i join orgs o on o.fyle_org_id = i.org_id
)
update integrations i
set org_name = o.name
from orgs o
where i.org_id = common_org_id;
