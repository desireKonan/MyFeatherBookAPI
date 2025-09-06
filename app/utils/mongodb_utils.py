from datetime import datetime
from typing import Dict, Any


def convert_datetime_to_iso(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert datetime objects to ISO format strings for MongoDB storage"""
    converted_data = data.copy()
    
    for key, value in converted_data.items():
        if isinstance(value, datetime):
            converted_data[key] = value.isoformat()
    
    return converted_data


def convert_iso_to_datetime(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert ISO format strings back to datetime objects from MongoDB"""
    converted_data = data.copy()
    
    # Remove MongoDB's _id field if present
    if '_id' in converted_data:
        converted_data['_id'] = str(converted_data['_id'])
    
    for key, value in converted_data.items():
        if isinstance(value, str) and key in ['created_at', 'updated_at']:
            try:
                # Handle both with and without timezone info
                if value.endswith('Z'):
                    converted_data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                else:
                    converted_data[key] = datetime.fromisoformat(value)
            except ValueError:
                # If conversion fails, keep the original string
                pass
    
    return converted_data
