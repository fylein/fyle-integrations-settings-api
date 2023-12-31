import requests
import logging
from workato import Workato

from apps.orgs.models import Org
from apps.orgs.exceptions import handle_workato_exception
from apps.travelperk.models import TravelPerk
from apps.names import TRAVELPERK

logger = logging.getLogger(__name__)
logger.level = logging.INFO


@handle_workato_exception(task_name = 'Travelperk Connection')
def connect_travelperk(org_id):
    connector = Workato()
    org = Org.objects.get(id=org_id)
    travelperk = TravelPerk.objects.get(org_id=org.id)
    connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
    connection_id = next(connection for connection in connections if connection['name'] == TRAVELPERK['connection'])['id']

    travelperk.travelperk_connection_id = connection_id
    travelperk.save()
    return connection_id


def download_file(remote_url, local_filename):
    # Send a GET request to the remote URL with streaming enabled
    response = requests.get(remote_url, stream=True)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Open a local file in binary write mode
        with open(local_filename, 'wb') as file:
            # Iterate over the content in chunks and write to the local file
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        # Print a success message if the file is downloaded successfully
        logger.log(f'Successfully downloaded the file to {local_filename}')
    else:
        # Print an error message if the file download fails
        logger.log(f'Failed to download the file. Status code: {response.status_code}')


def upload_to_s3_presigned_url(file_path, presigned_url):
    # Open the local file in binary read mode
    with open(file_path, 'rb') as file:
        # Send a PUT request to the S3 pre-signed URL with the file data
        response = requests.put(presigned_url, data=file)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Print a success message if the file is uploaded successfully
            logger.log(f'Successfully uploaded {file_path} to S3.')
        else:
            # Print an error message if the file upload fails
            logger.log(f'Failed to upload {file_path} to S3. Status code: {response.status_code}')
