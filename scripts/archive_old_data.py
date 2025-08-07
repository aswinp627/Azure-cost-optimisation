#This Python script moves old billing records (older than 3 months) from Azure Cosmos DB to Azure Blob Storage to save on storage and performance costs.

import datetime
import gzip
import json
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient, ContentSettings
 
# Configuration
COSMOS_ENDPOINT = "<COSMOS_DB_ENDPOINT>"
COSMOS_KEY = "<COSMOS_DB_KEY>"
DATABASE_NAME = "<DATABASE>"
CONTAINER_NAME = "<CONTAINER>"
 
BLOB_CONNECTION_STRING = "<BLOB_STORAGE_CONNECTION_STRING>"
BLOB_CONTAINER_NAME = "billing-archive"
 
# Init Cosmos DB client
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
db = cosmos_client.get_database_client(DATABASE_NAME)
container = db.get_container_client(CONTAINER_NAME)
 
# Init Blob client
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
 
# Step 1: Define archival cutoff date
cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=90)
 
# Step 2: Query old records
query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff_date.isoformat()}'"
old_records = list(container.query_items(query, enable_cross_partition_query=True))
 
# Step 3: Group and compress data
if old_records:
    year_month = cutoff_date.strftime("%Y-%m")
    blob_name = f"{year_month}/billing-archive.json.gz"
 
    compressed_data = gzip.compress(json.dumps(old_records, indent=2).encode("utf-8"))
 
    # Step 4: Upload to blob storage
    blob_container_client.upload_blob(
        name=blob_name,
        data=compressed_data,
        overwrite=True,
        content_settings=ContentSettings(content_type="application/gzip")
    )
 
    # Step 5: Delete from Cosmos DB
    for record in old_records:
        try:
            container.delete_item(item=record["id"], partition_key=record["customer_id"])
        except exceptions.CosmosHttpResponseError:
            print(f"Failed to delete record {record['id']}")
 
    print(f"Archived and deleted {len(old_records)} records to {blob_name}")
else:
    print("No records to archive.")
