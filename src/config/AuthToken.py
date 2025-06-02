import jwt
import datetime
from flask import request, jsonify
from functools import wraps

SECRET_KEY = "12345678"  

def gerar_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2) 
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def validar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        if not token:
            return jsonify({"message": "Token de autenticação é obrigatório"}), 401

        user_id = validar_token(token)
        if not user_id:
            return jsonify({"message": "Token inválido ou expirado"}), 401

        return f(user_id, *args, **kwargs)

    return decorated
