#!/usr/bin/env python3
"""
Script de migration de Firebase vers MongoDB
Ce script migre toutes les données des collections Firebase vers MongoDB
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.firebase_connector import firebase_connector
from app.mongodb_connector import mongodb_connector
from app.models.model import Note, Attachment, Synthesis
from app.repository.note_repository import NoteRepository
from app.repository.attachment_repository import AttachmentRepository
from app.repository.synthesis_repository import SynthesisRepository


def migrate_attachments():
    """Migrate attachments from Firebase to MongoDB"""
    print("Migrating attachments...")
    
    try:
        # Get all attachments from Firebase
        firebase_attachments = firebase_connector.get_collection('attachments').stream()
        
        migrated_count = 0
        for doc in firebase_attachments:
            data = doc.to_dict()
            attachment = Attachment.from_dict(data)
            
            # Create in MongoDB
            AttachmentRepository.create(attachment)
            migrated_count += 1
            print(f"Migrated attachment: {attachment.id}")
        
        print(f"Successfully migrated {migrated_count} attachments")
        
    except Exception as e:
        print(f"Error migrating attachments: {e}")


def migrate_syntheses():
    """Migrate syntheses from Firebase to MongoDB"""
    print("Migrating syntheses...")
    
    try:
        # Get all syntheses from Firebase
        firebase_syntheses = firebase_connector.get_collection('syntheses').stream()
        
        migrated_count = 0
        for doc in firebase_syntheses:
            data = doc.to_dict()
            synthesis = Synthesis.from_dict(data)
            
            # Create in MongoDB
            SynthesisRepository.create(synthesis)
            migrated_count += 1
            print(f"Migrated synthesis: {synthesis.id}")
        
        print(f"Successfully migrated {migrated_count} syntheses")
        
    except Exception as e:
        print(f"Error migrating syntheses: {e}")


def migrate_notes():
    """Migrate notes from Firebase to MongoDB"""
    print("Migrating notes...")
    
    try:
        # Get all notes from Firebase
        firebase_notes = firebase_connector.get_collection('note').stream()
        
        migrated_count = 0
        for doc in firebase_notes:
            data = doc.to_dict()
            note = Note.from_dict(data)
            
            # Create in MongoDB
            NoteRepository.create(note)
            migrated_count += 1
            print(f"Migrated note: {note.id}")
        
        print(f"Successfully migrated {migrated_count} notes")
        
    except Exception as e:
        print(f"Error migrating notes: {e}")


def main():
    """Main migration function"""
    print("Starting migration from Firebase to MongoDB...")
    print(f"Migration started at: {datetime.now()}")
    
    try:
        # Test connections
        print("Testing Firebase connection...")
        firebase_connector.db.collection('test').document('test').set({'test': True})
        print("Firebase connection OK")
        
        print("Testing MongoDB connection...")
        mongodb_connector.client.admin.command('ping')
        print("MongoDB connection OK")
        
        # Migrate in order: attachments first, then syntheses, then notes
        migrate_attachments()
        migrate_syntheses()
        migrate_notes()
        
        print("Migration completed successfully!")
        print(f"Migration finished at: {datetime.now()}")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
