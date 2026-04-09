from azure.cosmos import CosmosClient
import uuid
from datetime import datetime
import os


COSMOS_URI = os.getenv("COSMOS_URI")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE = os.getenv("COSMOS_DATABASE", "url_database")
COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER", "urls")

client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
database = client.get_database_client(COSMOS_DATABASE)
container = database.get_container_client(COSMOS_CONTAINER)


def save_scan(url, result):
    item = {
        "id": str(uuid.uuid4()),
        "user_id": "user123",
        "url": url,
        "is_suspicious": result["is_suspicious"],
        "risk_level": result["risk_level"],
        "score": result["score"],
        "reasons": result["reasons"],
        "created_at": str(datetime.utcnow())
    }

    container.create_item(body=item)


def get_scans(filter_type=None):
    if filter_type == "high":
        query = "SELECT * FROM c WHERE c.risk_level = 'High Risk'"
    elif filter_type == "safe":
        query = "SELECT * FROM c WHERE c.risk_level = 'Safe'"
    else:
        query = "SELECT * FROM c ORDER BY c.created_at DESC"

    return list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))