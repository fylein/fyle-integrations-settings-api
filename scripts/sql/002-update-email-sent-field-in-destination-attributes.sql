rollback;
begin;

update destination_attributes
set is_failure_email_sent = true
where detail->>'email' is null;