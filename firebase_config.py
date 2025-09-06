"""
Firebase Configuration Setup

To use Firebase with this project, you need to:

1. Install Firebase Admin SDK:
   pip install firebase-admin

2. Set up Firebase project:
   - Go to https://console.firebase.google.com/
   - Create a new project or select existing one
   - Go to Project Settings > Service Accounts
   - Generate new private key
   - Download the JSON file and save it as 'serviceAccountKey.json' in the project root

3. Alternative: Use environment variables for local development:
   - Set GOOGLE_APPLICATION_CREDENTIALS environment variable
   - Or use Firebase emulator for local development

4. Update requirements.txt:
   firebase-admin>=6.0.0
"""

import os

# Firebase configuration
FIREBASE_CONFIG = {
    'project_id': os.getenv('FIREBASE_PROJECT_ID', 'your-project-id'),
    'database_url': os.getenv('FIREBASE_DATABASE_URL', 'https://your-project-id.firebaseio.com'),
}

# Service account key file path
SERVICE_ACCOUNT_KEY_PATH = 'serviceAccountKey.json'

# Check if service account key exists
def check_firebase_setup():
    """Check if Firebase is properly configured"""
    if os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
        print("✅ Firebase service account key found")
        return True
    else:
        print("⚠️  Firebase service account key not found")
        print("Please download serviceAccountKey.json from Firebase Console")
        return False

if __name__ == "__main__":
    check_firebase_setup()
