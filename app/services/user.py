from cmath import log
from app.model.user import User
from flask_bcrypt import check_password_hash
from sqlalchemy.sql import text
from flask_bcrypt import generate_password_hash
from app import Session, session


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
            ok = check_password_hash(user.password, password) 
            if ok:
                user_serialized = User.serialize_login(user)
                return {'logged': True, 'user': user_serialized}
            return {'logged': False, 'message': 'Wrong credentials'}
        return {'logged': False, 'message': f'User {login} does not exists'}

            
    # ok = check_password_hash(hashed_password, password) # hashed_password from DB password string password of 


def create_user(user: User):
    pwd_hash = generate_password_hash(user.password).decode('utf-8')
    
    if pwd_hash:
        user.password = pwd_hash
    with Session.begin() as session:
        session.add(user)
        # session.commit()
    