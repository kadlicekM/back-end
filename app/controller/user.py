from app import app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from app.services.user import auth_user, confirm_users_registration,\
    get_all_active_users, get_all_pending_users, get_all_users, sign_up_user
from utils.user import send_registration_confirmed_mail


@app.route('/api/auth',methods=['POST'])
def auth():
    body = request.get_json()
    result, status_code = auth_user(body['login'], body['password'])
    is_logged = result['logged']
    if 'user' in result:
        access_token = create_access_token(result['user'])
        refresh_token = create_refresh_token(result['user'])
        return jsonify({'logged': is_logged, 'access_token': access_token, 'refresh_token': refresh_token}), status_code
    return jsonify({'logged': is_logged, 'message': result['message']}), status_code


@app.route('/api/user/sign-up', methods=['POST'])
def sign_up():
    body = request.get_json()
    result, status_code = sign_up_user(body)
    return jsonify(result), status_code


@app.route('/api/user/sign-up/confirm', methods=['POST'])
@jwt_required()
def confirm_registration():
    body = request.get_json()
    result, status_code = confirm_users_registration(body['user_id'])
    return jsonify(result), status_code


@app.route('/api/users/pending', methods=['GET'])
@jwt_required()
def get_all_pending():
    result, status_code = get_all_pending_users()
    return jsonify(result), status_code


@app.route('/api/users/activated', methods=['GET'])
@jwt_required()
def get_all_activated():
    result, status_code = get_all_active_users()
    return jsonify(result), status_code


@app.route('/api/users/all', methods=['GET'])
@jwt_required()
def get_all():
    result, status_code = get_all_users()
    return jsonify(result), status_code

