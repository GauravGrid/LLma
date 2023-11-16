import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from . import keys





class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False

        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return False

        try:
            jwt.decode(token, keys.JWT_SECRET, algorithms=['HS256'])
            return True
        except jwt.exceptions.InvalidTokenError:
            return False


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
     
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

 
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return None

        try:
            data = jwt.decode(token, keys.JWT_SECRET, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        return (data['username'], None)
    