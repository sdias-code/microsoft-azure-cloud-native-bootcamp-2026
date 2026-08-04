import uuid

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

from config import ACCOUNT_URL, CONTAINER_NAME


def upload_image_to_blob(file):
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)

    try:
        blob_service_client.create_container(CONTAINER_NAME)
    except ResourceExistsError:
        pass
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    blob_name = f"{uuid.uuid4()}.jpg"
    blob_client = container_client.get_blob_client(blob_name)

    blob_client.upload_blob(file.read(), overwrite=True)
    return f"{ACCOUNT_URL}/{CONTAINER_NAME}/{blob_name}"
