DROP FUNCTION if exists delete_workspace;

CREATE OR REPLACE FUNCTION delete_workspace(IN _org_id integer) RETURNS void AS $$
DECLARE
    rcount integer;
BEGIN
    RAISE NOTICE 'Deleting data from orgs %', _org_id;

    DELETE
    FROM bamboohr bh
    WHERE bh.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % bamboohr', rcount;

    DELETE
    FROM configurations c
    WHERE c.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % configurations', rcount;

    DELETE
    FROM fyle_credentials fc
    WHERE fc.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % fyle_credentials', rcount;

    DELETE
    FROM auth_tokens aut
    WHERE aut.user_id IN (
        SELECT u.id FROM users u WHERE u.id IN (
            SELECT ou.user_id FROM orgs_user ou WHERE org_id = _org_id
        )
    );
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % auth_tokens', rcount;

    DELETE
    FROM orgs_user ou
    WHERE org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % orgs user', rcount;

    DELETE
    FROM users u
    WHERE u.id IN (
        SELECT ou.user_id FROM orgs_user ou WHERE org_id = _org_id
    );
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % users', rcount;

    DELETE
    FROM orgs o
    WHERE o.id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % orgs', rcount;

RETURN;
END
$$ LANGUAGE plpgsql;
