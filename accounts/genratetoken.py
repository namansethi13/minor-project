from jose import jwt
from datetime import datetime, timedelta

def generate_jwt_token(payload, secret_key, expiration_time_minutes=1440):
    expiration = datetime.utcnow() + timedelta(minutes=expiration_time_minutes)
    
    # Create the JWT token with the payload and expiration time
    token = jwt.encode({'exp': expiration, 'payload':payload}, secret_key, algorithm='HS256')
    
    return token