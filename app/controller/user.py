from app import app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from app.services.user import auth_user, change_users_active_state,\
    get_all_active_users, get_all_pending_users, get_all_users, sign_up_user


@app.route('/api/auth',methods=['POST'])
def auth():
    body = request.get_json()
    result, status_code = auth_user(body['login'], body['password'])
    is_logged = result['logged']
    uid = result['uid'] if 'uid' in result else None
    if 'user' in result:
        access_token = create_access_token(result['user'])
        refresh_token = create_refresh_token(result['user'])
        return jsonify({'logged': is_logged, 'uid': uid, 'access_token': access_token, 'refresh_token': refresh_token}), status_code
    return jsonify({'logged': is_logged, 'message': result['message']}), status_code
    

@app.route('/api/user/sign-up', methods=['POST'])
def sign_up():
    body = request.get_json()
    result, status_code = sign_up_user(body)
    return jsonify(result), status_code


@app.route('/api/user/activate/<is_active>', methods=['POST'])
@jwt_required()
def change_active_state(is_active: str):
    body = request.get_json()
    result, status_code = change_users_active_state(body['user_id'], is_active == 'true')
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

