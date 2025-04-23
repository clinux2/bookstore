from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client.test_database

def test_connection():
    try:
        # Test connection by listing databases
        print("Connected to MongoDB!")
        print("Available databases:", client.list_database_names())
        
        # Create a test collection
        test_collection = db.test_collection
        
        # Insert a test document
        test_doc = {"name": "Test Document", "value": 123}
        result = test_collection.insert_one(test_doc)
        print(f"Inserted document with ID: {result.inserted_id}")
        
        # Read the document
        found_doc = test_collection.find_one({"name": "Test Document"})
        print("Found document:", found_doc)
        
        # Update the document
        test_collection.update_one(
            {"name": "Test Document"},
            {"$set": {"value": 456}}
        )
        print("Document updated")
        
        # Read the updated document
        updated_doc = test_collection.find_one({"name": "Test Document"})
        print("Updated document:", updated_doc)
        
        # Delete the document
        test_collection.delete_one({"name": "Test Document"})
        print("Document deleted")
        
        return True
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return False

if __name__ == "__main__":
    test_connection() 