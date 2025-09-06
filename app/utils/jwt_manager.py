# app/auth/jwt_manager.py
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import os

class JWTManager:
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
        self.algorithm = 'HS256'
        self.expiration_hours = 24
    
    def generate_token(self, user_id, username, role='user'):
        """Générer un token JWT"""
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=self.expiration_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token):
        """Vérifier un token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def hash_password(self, password):
        """Hasher un mot de passe"""
        return generate_password_hash(password)
    
    def check_password(self, password, hashed):
        """Vérifier un mot de passe"""
        return check_password_hash(hashed, password)

# Instance globale
jwt_manager = JWTManager()

def token_required(f):
    """Décorateur pour protéger les routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Vérifier l'en-tête Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Token malformé'}), 401
        
        if not token:
            return jsonify({'error': 'Token manquant'}), 401
        
        try:
            data = jwt_manager.verify_token(token)
            if data is None:
                return jsonify({'error': 'Token invalide ou expiré'}), 401
            
            # Ajouter les données utilisateur à la requête
            request.current_user = data
        except Exception as e:
            return jsonify({'error': 'Token invalide'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Décorateur pour les routes admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user') or request.current_user.get('role') != 'admin':
            return jsonify({'error': 'Accès refusé - Privilèges admin requis'}), 403
        return f(*args, **kwargs)
    
    return decorated