from typing import Dict, List
from app.model.user import User
from flask_bcrypt import check_password_hash
#from sqlalchemy.sql import text
from flask_bcrypt import generate_password_hash
from app import Session, session
from utils.user import send_registration_confirmed_mail


# def auth_user(user: User):
def auth_user(login: str, password: str):
    # query = text(f'SELECT * FROM USER_TABLE WHERE LOGIN={login}')
    # with engine.connect() as con:
    #     rs = con.execute(query)
    #     for row in rs:
    #         print(row)

    with Session.begin() as session:
    # with session.begin():
        user: User = session.query(User).filter(User.login == login).first()
    
        if user:
            ok = check_password_hash(user.password, password)   # bcrypt function to compare passwords
            if ok:
                user_serialized = User.serialize_token_payload(user)    #serialize_login 
                return {'logged': True, 'user': user_serialized}, 200
            return {'logged': False, 'message': 'Wrong credentials'}, 401
        return {'logged': False, 'message': f'User {login} does not exists'}, 401

def sign_up_user(request_data: Dict):
    login = request_data['login'] 
    password = request_data['password']
    name = request_data["name"]
    surname = request_data["surname"]
    email = request_data["email"]
    with session.begin():
        user: User = session.query(User).filter(User.login == login).first()
    if user: #Todo check if user is without error if out of context manager scope
        return {'status': False, 'message': f'User with login {login} already exists'}, 409
    pwd_hash = generate_password_hash(password).decode('utf-8')
    if not pwd_hash:
        return {'status': False, 'message': f'Error occured while creating new user'}, 500
    user_to_add = User(login=login, password=pwd_hash, name=name, surname= surname,  active=False, role= "user", email=email)
    with  session:
        session.add(user_to_add) 
        session.commit()
        session.close()
    if user_to_add: #Todo check if user is without error if out of context manager scope
        return {'status': True, 'message': f'Registration succeeded, please wait for confirmation e-mail'}, 201
    else: 
        return {'status': True, 'message': f'ELSEEEE'}, 201
        


def confirm_users_registration(requested_data: Dict):
    user_id=requested_data["used_id"]
    with session.begin():
        user: User = session.query(User).filter(User.id == user_id).first()
    if not user:
        return {'status': False, 'message': f'User could not be found'}, 404
    
    with session.begin():
        user.active = True
        # session.add(user) 
    if user:
        # Todo send user an informational email
        if not user.email:
            return {'status': True, 'message': f'Confirmed registration for user with id: {user_id}, but no email found'}, 200
        is_sent = send_registration_confirmed_mail(user.email)
        email_msg = 'Confirmation mail could not be sent.' if not is_sent else ''
        return {'status': True, 'message': f'Confirmed registration for user with id: {user_id}. {email_msg}'}, 200
    return {'status': False, 'message': f'Could not confirm registration for user with id: {user_id}'}, 500


def get_all_pending_users():
    with session.begin():
        users: List[User] = session.query(User).filter(User.active == False).all()
    if not users:
        return {'found': False, 'message': f'No pending users found'}, 404
    return {'found': True, 'users': [User.serialize_user(user) for user in users]}, 200


def get_all_active_users():
    with session.begin():
        users: List[User] = session.query(User).filter(User.active == True).all()
    if not users:
        return {'found': False, 'message': f'No active users found'}, 404
    return {'found': True, 'users': [User.serialize_user(user) for user in users]}, 200

def get_all_users():
    with session.begin():
        users: List[User] = session.query(User).all()
    if not users:
        return {'found': False, 'message': f'No users found'}, 404
    return {'found': True, 'users': [User.serialize_user(user) for user in users]}, 200