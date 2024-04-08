from functools import wraps
from jose import jwt
from django.conf import settings
from django.http import JsonResponse
from os import getenv
from .models import customUser
def jwt_token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Extract the JWT token from the request
        token = request.COOKIES.get('token')

        if token:
            try:
                # Decode and verify the JWT token
                payload = jwt.decode(token, getenv('jwt_key'), algorithms=['HS256'])
                # Attach the decoded payload to the request for further processing
                request.jwt_payload = payload
                email = payload['payload']
                user = customUser.objects.get(email=email)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.JWTError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
            except customUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Token required'}, status=401)

    return wrapper