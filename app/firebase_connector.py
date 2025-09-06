import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

class FirebaseConnector:
    """Firebase connector for Firestore database"""
    
    def __init__(self):
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase connection"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                print('Firebase config !')
                # Initialize Firebase with service account key
                # You can either use a service account file or environment variables
                print(os.path.exists('myfeatherbook-firebase-adminsdk-fbsvc-819a3ea30c.json'))
                if os.path.exists('myfeatherbook-firebase-adminsdk-fbsvc-819a3ea30c.json'):
                    cred = credentials.Certificate('myfeatherbook-firebase-adminsdk-fbsvc-819a3ea30c.json')
                    print(cred.get_credential()._token_uri)
                else:
                    # Use default credentials (for local development)
                    cred = credentials.ApplicationDefault()
                
                firebase_admin.initialize_app(cred)
            
            # Get Firestore client
            self.db = firestore.client()
            
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            raise
    
    def get_collection(self, collection_name):
        """Get a Firestore collection reference"""
        return self.db.collection(collection_name)
    
    def get_document(self, collection_name, document_id):
        """Get a specific document from Firestore"""
        return self.db.collection(collection_name).document(document_id)
    
    def add_document(self, collection_name, data):
        """Add a new document to a collection"""
        return self.db.collection(collection_name).add(data)
    
    def update_document(self, collection_name, document_id, data):
        """Update an existing document"""
        return self.db.collection(collection_name).document(document_id).update(data)
    
    def delete_document(self, collection_name, document_id):
        """Delete a document"""
        return self.db.collection(collection_name).document(document_id).delete()

# Global Firebase connector instance
firebase_connector = FirebaseConnector()

def initialize_firebase():
    """Initialize Firebase connection"""
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # Initialize Firebase with service account key
            # You can either use a service account file or environment variables
            if os.path.exists('myfeatherbook-firebase-adminsdk-fbsvc-819a3ea30c.json'):
                cred = credentials.Certificate('myfeatherbook-firebase-adminsdk-fbsvc-819a3ea30c.json')
            else:
                # Use default credentials (for local development)
                cred = credentials.ApplicationDefault()
            
            firebase_admin.initialize_app(cred)
        
        # Get Firestore client
        db = firestore.client()
        print("Firebase initialized successfully")
        return db
        
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        raise
