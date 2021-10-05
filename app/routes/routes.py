from app import app

from ..views import users
from ..views import helpers


@app.route('/auth', methods=['POST'])
def authenticate():
    return helpers.auth()

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return users.get_user(id)

@app.route('/users', methods=['GET'])
def get_users():
    return users.get_users()

@app.route('/users', methods=['POST'])
def post_user():
    return users.post_user()

@app.route('/users/<int:id>', methods=['PUT'])
@helpers.token_required
def update_user(id):
    return users.update_user(id)
    
@app.route('/users/<int:id>', methods=['DELETE'])
@helpers.token_required
def delete_user(id):
    return users.delete_user(id)