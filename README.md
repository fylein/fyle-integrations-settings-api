
# Fyle Integrations Settings API
Django Rest Framework API for Fyle integrations settings API

### Setup

* Download and install Docker desktop for Mac from [here.](https://www.docker.com/products/docker-desktop)

* If you're using a linux machine, please download docker according to the distrubution you're on.

* Follow the steps mentioned in fyle-integrations-central. Name of this service would be `admin-settings-api`

* Dev should be able to build, run services on few taps, even generating migration files, tailing logs, running tests, creating db fixture for unit test, etc are supported.

* You can also run tests using fyle-integrations-central, make sure to change the sql fixture file everytime to add some migrations

* Right Now We support integrations with
    1. BambooHr
    2. Travelperk


# Initiate Webhook for prod

* Bash into settings api worker container

* Now you can run the script written using the following commands
    python webhook_tests/executor.py {test_file_name} {org_id}

    1. test_file_name is the name of the file, it can be
        a. booker
        b. card_holder
        c. traveller
        d. default_admin
    2. org_id is the org_id of the account you are testing.

* Example of a sample run is
    python webhook_tests/executor.py booker 123

* Make sure to follow the steps mentioned in the test cases file, to simulate the behaviour.

* You can edit the payload to change the values of email, expense date, booker, traveller etc.
