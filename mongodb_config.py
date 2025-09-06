import os
from typing import Optional

class MongoDBConfig:
    """Configuration class for MongoDB connection"""
    
    def __init__(self):
        self.mongodb_uri: str = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.database_name: str = os.getenv('MONGODB_DATABASE', 'feather_book')
        self.max_pool_size: int = int(os.getenv('MONGODB_MAX_POOL_SIZE', '100'))
        self.min_pool_size: int = int(os.getenv('MONGODB_MIN_POOL_SIZE', '10'))
        self.max_idle_time_ms: int = int(os.getenv('MONGODB_MAX_IDLE_TIME_MS', '30000'))
        self.server_selection_timeout_ms: int = int(os.getenv('MONGODB_SERVER_SELECTION_TIMEOUT_MS', '5000'))
    
    def get_connection_string(self) -> str:
        """Get the complete MongoDB connection string with options"""
        options = [
            f"maxPoolSize={self.max_pool_size}",
            f"minPoolSize={self.min_pool_size}",
            f"maxIdleTimeMS={self.max_idle_time_ms}",
            f"serverSelectionTimeoutMS={self.server_selection_timeout_ms}"
        ]
        
        separator = "&" if "?" in self.mongodb_uri else "?"
        return f"{self.mongodb_uri}{separator}{'&'.join(options)}"

# Global configuration instance
mongodb_config = MongoDBConfig()
