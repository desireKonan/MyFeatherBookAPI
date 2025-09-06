"""
Factory pour créer les instances des repositories
"""

from app.repository.note_repository import NoteRepository
from app.repository.synthesis_repository import SynthesisRepository
from app.repository.user_repository import UserRepository

class RepositoryFactory:
    """Factory pour créer les instances des repositories"""
    
    def __init__(self):
        self._note_repository = None
        self._synthesis_repository = None
        self._user_repository = None
    
    @property
    def note_repository(self) -> NoteRepository:
        """Récupérer l'instance du NoteRepository"""
        if self._note_repository is None:
            self._note_repository = NoteRepository()
        return self._note_repository
    
    @property
    def synthesis_repository(self) -> SynthesisRepository:
        """Récupérer l'instance du SynthesisRepository"""
        if self._synthesis_repository is None:
            self._synthesis_repository = SynthesisRepository()
        return self._synthesis_repository

    @property
    def user_repository(self) -> UserRepository:
        """Récupérer l'instance du SynthesisRepository"""
        if self._user_repository is None:
            self._user_repository = UserRepository()
        return self._user_repository
    
    def reset(self):
        """Réinitialiser les instances (utile pour les tests)"""
        self._note_repository = None
        self._synthesis_repository = None
        self._user_repository = None


# Instance globale de la factory
repository_factory = RepositoryFactory()