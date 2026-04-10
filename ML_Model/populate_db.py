import pandas as pd
import uuid
from azure.cosmos import CosmosClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

COSMOS_URI = os.getenv("COSMOS_URI")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DB = os.getenv("COSMOS_DB")
COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER")

# Connect to Cosmos
client = CosmosClient(url=COSMOS_URI, credential=COSMOS_KEY)
database = client.get_database_client(COSMOS_DB)
container = database.get_container_client(COSMOS_CONTAINER)

# Load dataset
df = pd.read_csv("C:\Users\agasy\cloud\ML_Model\Data\url_features_extracted1.csv")  # replace with your filename

# Iterate and upload
for _, row in df.iterrows():
    url = row['URL']
    label = row['ClassLabel']
    
    item = {
        "id": str(uuid.uuid4()),
        "url": url,
        "is_suspicious": True if label == 0 else False,
        "risk_level": "High" if label == 0 else "Safe",
        "score": 100 if label == 0 else 0,
        "reasons": ["Phishing"] if label == 0 else [],
        "created_at": pd.Timestamp.now().isoformat()
    }
    try:
        container.create_item(body=item)
    except Exception as e:
        print(f"Failed to insert {url}: {e}")

print("Dataset upload complete!")