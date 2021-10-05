from datetime import datetime, timedelta

import jwt
from flask import request
from functools import wraps
from werkzeug.security import check_password_hash

from app import app
from .users import get_user_by_username


def auth():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return {
            'message': 'Dados de autenticação não informados.',
            'WWW-Authenticate': 'Basic auth="Login required"'
        }, 401

    user = get_user_by_username(auth.username)

    if not user:
        return {
            'message': 'Esse usuário não existe.',
            'data': {}
        }, 401

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.now() + timedelta(hours=12)
        }, app.config['SECRET_KEY'])

        return {
            'message': 'Usuário autenticado com sucesso.',
            'token': token,
            'exp': datetime.now() + timedelta(hours=12)
        }

    return {
        'message': 'Usuário ou senha incorretos.',
        'WWW-Authenticate': 'Basic auth="Login required"'
    }, 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return {
                'message': 'Token não informado.',
                'data': {}
            }, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = get_user_by_username(data['username'])
        except:
            return {
                'message': 'Token inválido ou expirado',
                'data': {}
            }, 401

        return f(current_user, *args, **kwargs)

    return decorated