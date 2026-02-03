import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variable
uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError("MONGODB_URI environment variable is not set")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["e_learning_platform"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
