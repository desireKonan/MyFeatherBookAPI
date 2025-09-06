"""
Example usage of Firebase models for Attachment, Note, and Synthesis
"""

from app.models import AttachmentType, Attachment, Note, Synthesis

def example_usage():
    """Example of how to use the Firebase models"""
    
    # Create a note
    note = Note(content="This is a sample note with attachments")
    
    # Create attachments
    audio_attachment = Attachment(
        url="https://example.com/audio.mp3",
        type=AttachmentType.AUDIO
    )
    
    document_attachment = Attachment(
        url="https://example.com/document.pdf",
        type=AttachmentType.DOCUMENT
    )
    
    # Add attachments to note
    note.add_attachment(audio_attachment)
    note.add_attachment(document_attachment)
    
    # Save note to Firebase (this will also save attachments)
    note.save()
    print(f"Note saved with ID: {note.id}")
    
    # Create a synthesis
    synthesis = Synthesis(
        url="https://example.com/synthesis.pdf",
        is_generated=True
    )
    
    # Save synthesis to Firebase
    synthesis.save()
    print(f"Synthesis saved with ID: {synthesis.id}")
    
    # Retrieve note by ID
    retrieved_note = Note.get_by_id(note.id)
    if retrieved_note:
        print("Retrieved Note:", retrieved_note.to_dict())
    
    # Retrieve synthesis by ID
    retrieved_synthesis = Synthesis.get_by_id(synthesis.id)
    if retrieved_synthesis:
        print("Retrieved Synthesis:", retrieved_synthesis.to_dict())
    
    # Get all notes
    all_notes = Note.get_all()
    print(f"Total notes in database: {len(all_notes)}")
    
    # Get all syntheses
    all_syntheses = Synthesis.get_all()
    print(f"Total syntheses in database: {len(all_syntheses)}")
    
    # Update note content
    if retrieved_note:
        retrieved_note.content = "Updated content"
        retrieved_note.save()
        print("Note updated successfully")
    
    # Delete synthesis
    if retrieved_synthesis:
        retrieved_synthesis.delete()
        print("Synthesis deleted successfully")

if __name__ == "__main__":
    example_usage()