#!/usr/bin/env python3
"""
Script de test pour vérifier que les repositories MongoDB fonctionnent correctement
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.model import Note, Attachment, Synthesis, AttachmentType
from app.repository.note_repository import NoteRepository
from app.repository.attachment_repository import AttachmentRepository
from app.repository.synthesis_repository import SynthesisRepository


def test_attachment_repository():
    """Test AttachmentRepository"""
    print("Testing AttachmentRepository...")
    
    try:
        # Create test attachment
        attachment = Attachment(
            url="https://example.com/test.mp3",
            type=AttachmentType.AUDIO,
            note_id="test-note-id"
        )
        
        # Test create
        created_attachment = AttachmentRepository.create(attachment)
        print(f"✓ Created attachment: {created_attachment.id}")
        
        # Test get_by_id
        retrieved_attachment = AttachmentRepository.get_by_id(created_attachment.id)
        assert retrieved_attachment is not None
        assert retrieved_attachment.url == attachment.url
        print(f"✓ Retrieved attachment: {retrieved_attachment.id}")
        
        # Test update
        retrieved_attachment.url = "https://example.com/updated.mp3"
        updated_attachment = AttachmentRepository.update(retrieved_attachment)
        assert updated_attachment.url == "https://example.com/updated.mp3"
        print(f"✓ Updated attachment: {updated_attachment.id}")
        
        # Test list_by_note
        attachments = AttachmentRepository.list_by_note("test-note-id")
        assert len(attachments) == 1
        print(f"✓ Listed attachments by note: {len(attachments)} found")
        
        # Test delete
        AttachmentRepository.delete(created_attachment.id)
        deleted_attachment = AttachmentRepository.get_by_id(created_attachment.id)
        assert deleted_attachment is None
        print(f"✓ Deleted attachment: {created_attachment.id}")
        
        print("AttachmentRepository tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ AttachmentRepository test failed: {e}")
        return False


def test_synthesis_repository():
    """Test SynthesisRepository"""
    print("Testing SynthesisRepository...")
    
    try:
        # Create test synthesis
        synthesis = Synthesis(
            url="https://example.com/synthesis.pdf",
            is_generated=True
        )
        
        # Test create
        created_synthesis = SynthesisRepository.create(synthesis)
        print(f"✓ Created synthesis: {created_synthesis.id}")
        
        # Test get_by_id
        retrieved_synthesis = SynthesisRepository.get_by_id(created_synthesis.id)
        assert retrieved_synthesis is not None
        assert retrieved_synthesis.url == synthesis.url
        print(f"✓ Retrieved synthesis: {retrieved_synthesis.id}")
        
        # Test update
        retrieved_synthesis.url = "https://example.com/updated-synthesis.pdf"
        updated_synthesis = SynthesisRepository.update(retrieved_synthesis)
        assert updated_synthesis.url == "https://example.com/updated-synthesis.pdf"
        print(f"✓ Updated synthesis: {updated_synthesis.id}")
        
        # Test list_all
        syntheses = SynthesisRepository.list_all()
        assert len(syntheses) >= 1
        print(f"✓ Listed all syntheses: {len(syntheses)} found")
        
        # Test delete
        SynthesisRepository.delete(created_synthesis.id)
        deleted_synthesis = SynthesisRepository.get_by_id(created_synthesis.id)
        assert deleted_synthesis is None
        print(f"✓ Deleted synthesis: {created_synthesis.id}")
        
        print("SynthesisRepository tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ SynthesisRepository test failed: {e}")
        return False


def test_note_repository():
    """Test NoteRepository"""
    print("Testing NoteRepository...")
    
    try:
        # Create test attachments
        attachment1 = Attachment(
            url="https://example.com/audio1.mp3",
            type=AttachmentType.AUDIO
        )
        attachment2 = Attachment(
            url="https://example.com/doc1.pdf",
            type=AttachmentType.DOCUMENT
        )
        
        # Create test note with attachments
        note = Note(
            content="Test note content",
            attachments=[attachment1, attachment2]
        )
        
        # Test create
        created_note = NoteRepository.create(note)
        print(f"✓ Created note: {created_note.id}")
        
        # Test get_by_id
        retrieved_note = NoteRepository.get_by_id(created_note.id)
        assert retrieved_note is not None
        assert retrieved_note.content == note.content
        assert len(retrieved_note.attachments) == 2
        print(f"✓ Retrieved note: {retrieved_note.id}")
        
        # Test update
        retrieved_note.content = "Updated note content"
        updated_note = NoteRepository.update(retrieved_note)
        assert updated_note.content == "Updated note content"
        print(f"✓ Updated note: {updated_note.id}")
        
        # Test list_all
        notes = NoteRepository.list_all()
        assert len(notes) >= 1
        print(f"✓ Listed all notes: {len(notes)} found")
        
        # Test delete
        NoteRepository.delete(created_note.id)
        deleted_note = NoteRepository.get_by_id(created_note.id)
        assert deleted_note is None
        print(f"✓ Deleted note: {created_note.id}")
        
        print("NoteRepository tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ NoteRepository test failed: {e}")
        return False


def main():
    """Main test function"""
    print("Starting MongoDB repositories tests...")
    print(f"Tests started at: {datetime.now()}")
    print("-" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_attachment_repository():
        tests_passed += 1
    print("-" * 50)
    
    if test_synthesis_repository():
        tests_passed += 1
    print("-" * 50)
    
    if test_note_repository():
        tests_passed += 1
    print("-" * 50)
    
    # Results
    print(f"Tests completed: {tests_passed}/{total_tests} passed")
    print(f"Tests finished at: {datetime.now()}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! MongoDB repositories are working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
