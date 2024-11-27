rollback;
begin;

-- count: 309
update orgs set allow_dynamics='t' where allow_dynamics='f';