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
    FROM travelperk t
    WHERE t.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % travelperk', rcount;

    DELETE
    FROM bamboohr_configurations bc
    WHERE bc.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % bamboohr_configurations', rcount;

    DELETE
    FROM travelperk_credentials tcd
    WHERE tcd.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % travelperk_credentials', rcount;

    DELETE
    FROM invoice_line_items ilt
    WHERE ilt.invoice_id IN (
        SELECT il.id FROM invoices il WHERE il.org_id = _org_id
    );
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % invoice_line_items', rcount;

    DELETE
    FROM invoices i
    WHERE i.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % invoices', rcount;

    DELETE
    FROM travelperk_configurations tc
    WHERE tc.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % travelperk_configurations', rcount;

    DELETE
    FROM fyle_credentials fc
    WHERE fc.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % fyle_credentials', rcount;

    DELETE
    FROM travelperk_profile_mappings tpm
    WHERE tpm.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % travelperk_profile_mappings', rcount;

    DELETE
    FROM imported_expense_details ied
    WHERE ied.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % imported_expense_details', rcount;

    DELETE
    FROM travelperk_advanced_settings tas
    WHERE tas.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % travelperk_advanced_settings', rcount;

    DELETE
    FROM expense_attributes ea
    WHERE ea.org_id = _org_id;
    GET DIAGNOSTICS rcount = ROW_COUNT;
    RAISE NOTICE 'Deleted % expense_attributes', rcount;

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
