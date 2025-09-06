# Feather Book API

Une API REST moderne pour la gestion des notes, pièces jointes et synthèses avec Firebase et documentation Swagger automatique.

## 🚀 Fonctionnalités

- **API REST complète** avec Flask-RESTX
- **Documentation Swagger automatique** accessible via `/swagger/`
- **Intégration Firebase** pour le stockage des données
- **Gestion des notes** avec pièces jointes
- **Gestion des synthèses**
- **Validation des données** automatique
- **Gestion d'erreurs** standardisée
- **CORS activé** pour les applications frontend
- **Système de logging avancé** avec rotation des fichiers et couleurs
- **Middleware de logging automatique** pour toutes les requêtes HTTP
- **Mesure des performances** intégrée
- **Configuration par environnement** (dev/prod/test)

## 📋 Prérequis

- Python 3.8+
- Firebase project configuré
- Service account key pour Firebase (optionnel pour le développement local)

## 🛠️ Installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd my-feather-book-api
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration Firebase** (optionnel pour le développement)
   - Placez votre fichier `serviceAccountKey.json` à la racine du projet
   - Ou configurez les variables d'environnement Firebase

## 🚀 Démarrage

```bash
python main.py
```

L'API sera accessible sur `http://localhost:5000`

## 📚 Documentation Swagger

Une fois l'API démarrée, accédez à la documentation interactive :

- **URL principale** : `http://localhost:5000`
- **Documentation Swagger** : `http://localhost:5000/swagger/`
- **Health Check** : `http://localhost:5000/api/v1/health`

## 🔗 Endpoints API

### Notes (`/api/v1/notes`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/v1/notes` | Récupérer toutes les notes |
| POST | `/api/v1/notes` | Créer une nouvelle note |
| GET | `/api/v1/notes/{id}` | Récupérer une note par ID |
| PUT | `/api/v1/notes/{id}` | Mettre à jour une note |
| DELETE | `/api/v1/notes/{id}` | Supprimer une note |

### Synthèses (`/api/v1/syntheses`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/v1/notes` | Récupérer toutes les synthèses |
| POST | `/api/v1/notes` | Créer une nouvelle synthèse |
| GET | `/api/v1/notes/{id}` | Récupérer une synthèse par ID |
| DELETE | `/api/v1/notes/{id}` | Supprimer une synthèse |

### Health Check

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/v1/health` | Vérifier l'état de l'API |

## 📝 Exemples d'utilisation

### Créer une note avec pièces jointes

```bash
curl -X POST "http://localhost:5000/api/v1/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Ma note avec pièces jointes",
    "attachments": [
      {
        "url": "https://example.com/audio.mp3",
        "type": "AUDIO"
      },
      {
        "url": "https://example.com/document.pdf",
        "type": "DOCUMENT"
      }
    ]
  }'
```

### Récupérer toutes les notes

```bash
curl -X GET "http://localhost:5000/api/v1/notes"
```

### Créer une synthèse

```bash
curl -X POST "http://localhost:5000/api/v1/syntheses" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/synthesis.pdf",
    "is_generated": true
  }'
```

## 🏗️ Structure du projet

```
my-feather-book-api/
├── app/
│   ├── __init__.py              # Factory pattern pour Flask
│   ├── api.py                   # Configuration principale de l'API
│   ├── firebase_connector.py    # Connexion Firebase
│   ├── logger_config.py         # Configuration du système de logging
│   ├── middleware.py            # Middleware pour le logging automatique
│   ├── controllers/             # Contrôleurs séparés par domaine
│   │   ├── __init__.py          # Export des contrôleurs
│   │   ├── notes_controller.py  # Contrôleur pour les notes
│   │   ├── syntheses_controller.py # Contrôleur pour les synthèses
│   │   └── health_controller.py # Contrôleur pour le health check
│   ├── models/                  # Modèles de données
│   └── repository/              # Couche d'accès aux données
├── main.py                      # Point d'entrée de l'application
├── config.py                    # Configuration de l'application
├── env.example                  # Exemple de variables d'environnement
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation
```

## 🏗️ Architecture

### Structure modulaire
L'API est organisée en modules séparés pour une meilleure maintenabilité :

#### Contrôleurs (`app/controllers/`)
- **`notes_controller.py`** : Gestion complète des notes (CRUD)
- **`syntheses_controller.py`** : Gestion des synthèses (CRUD)
- **`health_controller.py`** : Health check de l'API

#### Avantages de cette architecture
- **Séparation des responsabilités** : Chaque contrôleur gère un domaine spécifique
- **Maintenabilité** : Code plus facile à maintenir et à tester
- **Évolutivité** : Ajout facile de nouveaux contrôleurs
- **Réutilisabilité** : Contrôleurs indépendants et réutilisables
- **Logging spécialisé** : Chaque contrôleur a son propre logger

#### Configuration de l'API (`app/api.py`)
- Centralise la configuration de Flask-RESTX
- Importe et enregistre tous les contrôleurs
- Configure la documentation Swagger

## 🔧 Configuration

### Variables d'environnement

Copiez le fichier `env.example` vers `.env` et configurez vos variables :

```bash
cp env.example .env
```

#### Configuration de base
- `FLASK_ENV` : Environnement Flask (development/production/testing)
- `SECRET_KEY` : Clé secrète pour l'application (obligatoire en production)

#### Configuration du logging
- `LOG_LEVEL` : Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_TO_FILE` : Activer la journalisation dans des fichiers (true/false)
- `LOG_TO_CONSOLE` : Activer la journalisation dans la console (true/false)
- `LOG_FORMAT` : Format des logs (detailed, simple, json)
- `LOG_MAX_FILE_SIZE` : Taille maximale des fichiers de log en bytes
- `LOG_BACKUP_COUNT` : Nombre de fichiers de sauvegarde à conserver

#### Configuration Firebase
- `GOOGLE_APPLICATION_CREDENTIALS` : Chemin vers le fichier de clé de service Firebase
- `FIREBASE_SERVICE_ACCOUNT_KEY` : Nom du fichier de clé de service Firebase

### Configuration Firebase

1. **Avec fichier de clé de service** :
   - Placez `serviceAccountKey.json` à la racine du projet

2. **Avec variables d'environnement** :
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/serviceAccountKey.json"
   ```

## 🧪 Tests

Pour tester l'API, vous pouvez utiliser :

1. **Swagger UI** : `http://localhost:5000/swagger/`
2. **cURL** : Voir les exemples ci-dessus
3. **Postman** : Importez les endpoints depuis Swagger
4. **Tests automatisés** : À implémenter

## 🚀 Déploiement

### Développement local
```bash
python main.py
```

### Production
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## 📊 Monitoring et Logging

### Health Check
- **Health Check** : `GET /api/v1/health`

### Système de Logging
L'API dispose d'un système de logging avancé avec :

#### Fichiers de logs
- `logs/feather_book_api.log` : Log principal de l'application
- `logs/feather_book_api_errors.log` : Log des erreurs uniquement
- `logs/feather_book_api_access.log` : Log des requêtes HTTP

#### Fonctionnalités
- **Rotation automatique** des fichiers de log (10MB par défaut)
- **Niveaux de log** configurables par environnement
- **Formats de log** : détaillé (dev), simple (test), JSON (prod)
- **Couleurs dans la console** pour une meilleure lisibilité
- **Logging automatique** de toutes les requêtes HTTP
- **Mesure des performances** de chaque opération
- **Contexte des erreurs** avec stack traces

#### Configuration par environnement
- **Développement** : Logs détaillés en console et fichier
- **Production** : Logs JSON en fichiers uniquement
- **Tests** : Logs simples en console uniquement

### Métriques
- **Temps de réponse** de chaque endpoint
- **Taux d'erreur** par endpoint
- **Performance des opérations** de base de données
- **Utilisation des ressources** (à implémenter)

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :

1. Consultez la documentation Swagger
2. Vérifiez les logs de l'application
3. Ouvrez une issue sur GitHub

---

**Feather Book API** - Une API moderne et documentée pour la gestion de contenu 📚
