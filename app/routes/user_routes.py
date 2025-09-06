# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from app.models.model import User
from app.repository.user_repository import UserRepository
from app.utils.jwt_manager import jwt_manager
from app.logger_config import get_logger
from app.middleware import log_function_call
import re

# Create blueprint for authentication
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# Get repository instance
user_repository = UserRepository()

def validate_email(email):
    """Valider le format email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Valider la force du mot de passe"""
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    if not re.search(r'[A-Z]', password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    
    if not re.search(r'[a-z]', password):
        return False, "Le mot de passe doit contenir au moins une minuscule"
    
    if not re.search(r'\d', password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"
    
    return True, "Mot de passe valide"

@auth_bp.route('/register', methods=['POST'])
@log_function_call('register_user')
def register():
    """Enregistrer un nouvel utilisateur"""
    logger = get_logger('auth_routes')
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données requises'}), 400
        
        # Validation des champs requis
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        # Validation de l'email
        if not validate_email(data['email']):
            return jsonify({'error': 'Format d\'email invalide'}), 400
        
        # Validation du mot de passe
        is_valid, message = validate_password(data['password'])
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Vérifier si l'utilisateur existe déjà
        if user_repository.get_by_username(data['username']):
            return jsonify({'error': 'Nom d\'utilisateur déjà utilisé'}), 409
        
        if user_repository.get_by_email(data['email']):
            return jsonify({'error': 'Email déjà utilisé'}), 409
        
        # Créer l'utilisateur
        user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        user.set_password(data['password'])
        
        user_repository.create(user)
        
        logger.info(f"Utilisateur créé avec succès: {user.username}")
        return jsonify(user.to_dict_with_token()), 201
        
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erreur lors de l\'enregistrement'}), 500

@auth_bp.route('/login', methods=['POST'])
@log_function_call('login_user')
def login():
    """Connexion utilisateur"""
    logger = get_logger('auth_routes')
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Nom d\'utilisateur et mot de passe requis'}), 400
        
        # Récupérer l'utilisateur
        user = user_repository.get_by_username(data['username'])
        if not user:
            logger.warning(f"Tentative de connexion avec un nom d'utilisateur inexistant: {data['username']}")
            return jsonify({'error': 'Identifiants invalides'}), 401
        
        # Vérifier le mot de passe
        if not user.check_password(data['password']):
            logger.warning(f"Tentative de connexion avec un mot de passe incorrect pour: {data['username']}")
            return jsonify({'error': 'Identifiants invalides'}), 401
        
        # Vérifier si le compte est actif
        if not user.is_active:
            logger.warning(f"Tentative de connexion avec un compte inactif: {data['username']}")
            return jsonify({'error': 'Compte inactif'}), 401
        
        # Mettre à jour la dernière connexion
        user_repository.update_last_login(user.id)
        
        logger.info(f"Connexion réussie: {user.username}")
        return jsonify(user.to_dict_with_token()), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erreur lors de la connexion'}), 500

@auth_bp.route('/me', methods=['GET'])
@log_function_call('get_current_user')
def get_current_user():
    """Récupérer les informations de l'utilisateur connecté"""
    from app.auth.jwt_manager import token_required
    
    @token_required
    def _get_current_user():
        return jsonify(request.current_user), 200
    
    return _get_current_user()

@auth_bp.route('/refresh', methods=['POST'])
@log_function_call('refresh_token')
def refresh_token():
    """Rafraîchir le token"""
    from app.auth.jwt_manager import token_required
    
    @token_required
    def _refresh_token():
        user_data = request.current_user
        new_token = jwt_manager.generate_token(
            user_data['user_id'],
            user_data['username'],
            user_data['role']
        )
        return jsonify({'token': new_token}), 200
    
    return _refresh_token()