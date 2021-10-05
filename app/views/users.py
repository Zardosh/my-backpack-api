from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.users import User, user_schema, users_schema


def get_user_by_username(username):
    user = db.session.query(User) \
        .filter(User.username == username) \
        .first()

    return user if user else None
    
def get_user_by_email(email):
    user = db.session.query(User) \
        .filter(User.email == email) \
        .first()

    return user if user else None

def get_user(id):
    user = db.session.query(User) \
        .filter(User.id == id) \
        .first()

    if user:
        result = user_schema.dump(user)
        
        return {
            'message': 'Usuário encontrado.',
            'data': result
        }, 201
    else:
        return {
            'message': 'Esse usuário não existe.',
            'data': {}
        }, 404

def get_users():
    users = db.session.query(User).all()

    if users:
        result = users_schema.dump(users)

        return {
            'message': 'Busca efetuada com sucesso.',
            'data': result
        }
    
    return {
        'message': 'Nenhum resultado encontrado.',
        'data': {}
    }

def post_user():
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']

    if get_user_by_username(username):
        return {
            'message': 'Esse nome de usuário já está em uso.',
            'data': {}
        }, 409
    elif get_user_by_email(email):
        return {
            'message': 'Esse email já está em uso.',
            'data': {}
        }, 409

    password_hash = generate_password_hash(password)
    user = User(username, password_hash, name, email)

    try:
        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user)

        return {
            'message': 'Usuário criado com sucesso.',
            'data': result
        }, 201
    except Exception as e:
        db.session.rollback()

        return {
            'message': 'Erro ao criar usuário.',
            'data': {}
        }, 500

def update_user(id):
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']

    user = db.session.query(User) \
        .filter(User.id == id) \
        .first()

    if not user:
        return {
            'message': 'Esse usuário não existe.',
            'data': {}
        }, 404

    is_username_in_use = db.session.query(User) \
        .filter(User.id != id,
                User.username == username) \
        .first()

    if is_username_in_use:
        return {
            'message': 'Esse nome de usuário já está em uso.',
            'data': {}
        }, 409

    is_email_in_use = db.session.query(User) \
        .filter(User.id != id,
                User.email == email) \
        .first()

    if is_email_in_use:
        return {
            'message': 'Esse email já está em uso.',
            'data': {}
        }, 409

    password_hash = generate_password_hash(password)

    try:
        user.username = username
        user.password = password_hash
        user.name = name
        user.email = email
        
        db.session.commit()

        result = user_schema.dump(user)

        return {
            'message': 'Usuário atualizado com sucesso.',
            'data': result
        }, 201
    except Exception as e:
        print(e)
        db.session.rollback()

        return {
            'message': 'Erro ao atualizar usuário.',
            'data': {}
        }, 500

def delete_user(id):
    user = db.session.query(User) \
        .filter(User.id == id) \
        .first()

    if not user:
        return {
            'message': 'Esse usuário não existe.',
            'data': {}
        }, 404

    try:
        db.session.delete(user)
        db.session.commit()

        result = user_schema.dump(user)

        return {
            'message': 'Usuário removido com sucesso.',
            'data': result
        }, 200
    except:
        db.session.rollback()

        return {
            'message': 'Não foi possível remover esse usuário.',
            'data': {}
        }, 500