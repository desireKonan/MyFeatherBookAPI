# Migration de Firebase vers MongoDB

Ce document explique comment migrer l'API Feather Book de Firebase vers MongoDB.

## Prérequis

1. MongoDB installé localement ou accès à une instance MongoDB (Atlas, etc.)
2. Python 3.7+
3. Les dépendances installées : `pip install -r requirements.txt`

## Configuration

### Variables d'environnement

Copiez le fichier `env.mongodb.example` vers `.env` et configurez les variables :

```bash
cp env.mongodb.example .env
```

Variables importantes :
- `MONGODB_URI` : URI de connexion MongoDB (par défaut : `mongodb://localhost:27017/`)
- `MONGODB_DATABASE` : Nom de la base de données (par défaut : `feather_book`)

### Exemple de configuration

Pour MongoDB local :
```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=feather_book
```

Pour MongoDB Atlas :
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=feather_book
```

## Migration des données

### Script de migration automatique

Un script de migration est fourni pour migrer automatiquement toutes les données de Firebase vers MongoDB :

```bash
python migrate_to_mongodb.py
```

Ce script :
1. Se connecte à Firebase et MongoDB
2. Migre les attachments
3. Migre les syntheses
4. Migre les notes
5. Affiche le progrès de la migration

### Migration manuelle

Si vous préférez migrer manuellement, vous pouvez utiliser les repositories MongoDB directement :

```python
from app.repository.note_repository import NoteRepository
from app.repository.attachment_repository import AttachmentRepository
from app.repository.synthesis_repository import SynthesisRepository

# Créer une note
note = Note(content="Ma note")
NoteRepository.create(note)
```

## Changements dans le code

### Connecteur de base de données

- **Ancien** : `app/firebase_connector.py`
- **Nouveau** : `app/mongodb_connector.py`

### Repositories

Tous les repositories ont été mis à jour pour utiliser MongoDB :

- `app/repository/note_repository.py`
- `app/repository/attachment_repository.py`
- `app/repository/synthesis_repository.py`

### Configuration

- **Ancien** : Configuration Firebase dans `firebase_config.py`
- **Nouveau** : Configuration MongoDB dans `mongodb_config.py`

## Structure des collections MongoDB

### Collection `notes`
```json
{
  "_id": "ObjectId",
  "id": "uuid-string",
  "content": "string",
  "attachments": ["attachment-id-1", "attachment-id-2"],
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

### Collection `attachments`
```json
{
  "_id": "ObjectId",
  "id": "uuid-string",
  "url": "string",
  "type": "Audio" | "Document",
  "note_id": "note-uuid-string",
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

### Collection `syntheses`
```json
{
  "_id": "ObjectId",
  "id": "uuid-string",
  "url": "string",
  "is_generated": boolean,
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

## Avantages de MongoDB

1. **Flexibilité** : Schéma flexible pour les documents
2. **Performance** : Indexation avancée et requêtes optimisées
3. **Scalabilité** : Horizontal scaling avec sharding
4. **Coût** : MongoDB Atlas offre un plan gratuit généreux
5. **Outils** : Meilleur support pour l'agrégation et l'analyse

## Tests

Pour tester la migration :

1. Démarrez MongoDB localement ou configurez Atlas
2. Exécutez le script de migration
3. Testez les endpoints de l'API
4. Vérifiez que les données sont correctement stockées

## Rollback

Si vous devez revenir à Firebase :

1. Restaurez les anciens fichiers de repository
2. Remplacez `mongodb_connector` par `firebase_connector` dans les imports
3. Redémarrez l'application

## Support

En cas de problème avec la migration, vérifiez :

1. La connexion MongoDB
2. Les variables d'environnement
3. Les logs d'erreur
4. La structure des données migrées
