DROP FUNCTION if exists delete_integration;

CREATE OR REPLACE FUNCTION delete_integration(IN _org_id varchar(255)) RETURNS void AS $$
DECLARE
    rcount integer;
BEGIN
    DELETE
    FROM integrations i
    WHERE i.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % integrations', rcount;

RETURN;
END
$$ LANGUAGE plpgsql;
