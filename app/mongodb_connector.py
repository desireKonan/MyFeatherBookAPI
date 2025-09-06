from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from datetime import datetime
import os
from typing import Optional
from mongodb_config import mongodb_config

class MongoDBConnector:
    """MongoDB connector for database operations"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self._initialize_mongodb()
    
    def _initialize_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            # Get MongoDB connection string from configuration
            mongodb_uri = mongodb_config.get_connection_string()
            database_name = mongodb_config.database_name
            
            # Create MongoDB client with configuration
            self.client = MongoClient(mongodb_uri)
            self.db = self.client[database_name]
            
            # Test connection
            self.client.admin.command('ping')
            print(f"MongoDB connected successfully to database: {database_name}")
            
        except Exception as e:
            print(f"Error initializing MongoDB: {e}")
            raise
    
    def get_collection(self, collection_name: str) -> Collection:
        """Get a MongoDB collection reference"""
        return self.db[collection_name]
    
    def get_database(self) -> Database:
        """Get the database reference"""
        return self.db
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

# Global MongoDB connector instance
mongodb_connector = MongoDBConnector()

def initialize_mongodb():
    """Initialize MongoDB connection"""
    try:
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        database_name = os.getenv('MONGODB_DATABASE', 'feather_book')
        
        client = MongoClient(mongodb_uri)
        db = client[database_name]
        
        # Test connection
        client.admin.command('ping')
        print(f"MongoDB initialized successfully to database: {database_name}")
        return db
        
    except Exception as e:
        print(f"Error initializing MongoDB: {e}")
        raise
