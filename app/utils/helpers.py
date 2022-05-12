import jwt
from app import app

#decode whole JWT, returns whole sub(login,user_id,user_token )
def decode_jwt_payload(request):
    token = request.headers['AUTHORIZATION'].split()[1]
    payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    return payload['sub']
#decode whole JWT, returns just user_id
def decode_jwt_user_id(request):
    token = request.headers['AUTHORIZATION'].split()[1]
    payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    return payload['sub']['user_id']