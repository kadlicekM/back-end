from app import app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from app.services.user import auth_user, create_user
from app.model.user import User

@app.route('/api/auth',methods=['POST'])
def auth():
    body = request.get_json()
    login = body['login']
    password = body['password']
    # user = User.auth(body)
    # print(user.login, user.password)
    result = auth_user(login ,password)
    is_logged = result['logged']
    if 'user' in result:
        access_token = create_access_token(result['user'])
        refresh_token = create_access_token(result['user'])
        return jsonify({'logged': is_logged, 'access_token': access_token, 'refresh_token': refresh_token})
    return jsonify({'logged': is_logged, 'message': result['message']})


@app.route('/api/user/add', methods=['POST'])
@jwt_required()
def add_user():
    body = request.get_json()
    user = User.add(body)
    create_user(user)
    return jsonify({'msg': 'Hola!'})
