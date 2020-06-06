import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')

## AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    authorize = request.headers.get('Authorization', None)
    if not authorize:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description':'Authorization in header is expected'
        }, 401)

    parts = authorize.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description':'The token sent does not start with bearer'
        }, 401)
    elif len(parts) != 2:
        raise AuthError({
            'code': 'token_malformed',
            'description':'The token is not formatted correctly'
        }, 401)

    token = parts[1]
    return token     

# Check JWT permissions
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code':'permissions_not_in_payload',
            'description':'Permissions not found in token'
        },401)
    if permission not in payload['permissions']:
        raise AuthError({
            'code':'requested_permission_not_allowed',
            'description':'You have requested a permission not allowed'
        },401)
    
    return True

# Parse and verify JWT
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code':'invalid_header',
            'description':'No key found in header'
    }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://'+AUTH0_DOMAIN+'/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token has expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code':'invalid_header',
                'description': 'Unable to locate the correct key'
            }, 400)
        


# Authorization decorator method accepts required permission as an input to validate against JWT
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                raise AuthError({
                    'code': 'authorization_header_missing',
                    'description':'Authorization in header is expected'
                }, 401)

            check_permissions(permission, payload)

            return f(*args, **kwargs) #payload, 

        return wrapper
    return requires_auth_decorator