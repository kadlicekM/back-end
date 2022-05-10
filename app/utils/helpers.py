import jwt
from app import app

def decode_jwt_payload(request):
    token = request.headers['AUTHORIZATION'].split()[1]
    payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    return payload['sub']

def decode_jwt_user_id(request):
    token = request.headers['AUTHORIZATION'].split()[1]
    payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    return payload['sub']['user_id']