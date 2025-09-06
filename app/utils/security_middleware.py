# app/middleware/security_middleware.py
from flask import request, jsonify, current_app
from functools import wraps
import time
from collections import defaultdict, deque
import re

class RateLimiter:
    """Limiteur de taux simple"""
    
    def __init__(self):
        self.requests = defaultdict(deque)
        self.max_requests = 100  # Requêtes par minute
        self.window_size = 60  # Secondes
    
    def is_allowed(self, client_ip):
        """Vérifier si la requête est autorisée"""
        now = time.time()
        client_requests = self.requests[client_ip]
        
        # Supprimer les requêtes anciennes
        while client_requests and client_requests[0] <= now - self.window_size:
            client_requests.popleft()
        
        # Vérifier la limite
        if len(client_requests) >= self.max_requests:
            return False
        
        # Ajouter la requête actuelle
        client_requests.append(now)
        return True

# Instance globale
rate_limiter = RateLimiter()

def rate_limit(f):
    """Décorateur pour limiter le taux de requêtes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        if not rate_limiter.is_allowed(client_ip):
            return jsonify({'error': 'Trop de requêtes, veuillez réessayer plus tard'}), 429
        
        return f(*args, **kwargs)
    
    return decorated

def validate_input(f):
    """Décorateur pour valider les entrées"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Vérifier les headers malveillants
        for header, value in request.headers:
            if re.search(r'<script|javascript:|on\w+\s*=', value, re.IGNORECASE):
                return jsonify({'error': 'Headers malveillants détectés'}), 400
        
        # Vérifier les paramètres de requête
        for key, value in request.args.items():
            if re.search(r'<script|javascript:|on\w+\s*=', str(value), re.IGNORECASE):
                return jsonify({'error': 'Paramètres malveillants détectés'}), 400
        
        return f(*args, **kwargs)
    
    return decorated

def security_headers(f):
    """Décorateur pour ajouter des headers de sécurité"""
    @wraps(f)
    def decorated(*args, **kwargs):
        response = f(*args, **kwargs)
        
        # Ajouter des headers de sécurité
        if hasattr(response, 'headers'):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['Content-Security-Policy'] = "default-src 'self'"
        
        return response
    
    return decorated