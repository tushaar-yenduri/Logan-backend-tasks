import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "student_db")

# Global client instance for connection pooling
_client = None

def get_client():
    """Returns a singleton MongoClient instance."""
    global _client
    if _client is None:
        try:
            _client = MongoClient(MONGO_URI)
            # Trigger a connection check
            _client.admin.command('ping')
            print(f"Successfully connected to MongoDB at {MONGO_URI}")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            _client = None
    return _client

def get_database():
    """Returns the database object using the singleton client."""
    client = get_client()
    if client:
        return client[DB_NAME]
    return None

def get_collection(collection_name="students"):
    """Returns a specific collection from the database."""
    db = get_database()
    if db is not None:
        return db[collection_name]
    return None

def close_connection():
    """Closes the MongoDB connection."""
    global _client
    if _client:
        _client.close()
        _client = None
        print("MongoDB connection closed.")
