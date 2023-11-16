from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import User
from passlib.hash import pbkdf2_sha256
from django.db.models import Q
import jwt
import datetime
from . import keys

@api_view(['POST'])
@permission_classes([AllowAny])

def signup(request):
    try:
        data = request.data if request.data is not None else {}
        required_fields = set(['username', 'email', 'password'])
        if not required_fields.issubset(data.keys()):
            return Response(status=400, data={'error': 'Missing required fields'})
        existing_user = User.objects.filter(Q(username=data['username']) | Q(email=data['email']))
        if existing_user:
            return Response(status=409, data={'error': 'User with the same username or email already exists'})
        password_hash = pbkdf2_sha256.hash(data['password'])
        user = {
            'username': data['username'],
            'email': data['email'],
            'password': str(password_hash)
        }
        serializer = UserSerializer(data = user)
        if serializer.is_valid():
            instance=serializer.save()
        token = jwt.encode({'username': data['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, keys.JWT_SECRET)
        return Response(status=status.HTTP_201_CREATED, data={'token': token, 'statusText': 'User Created'})
    except Exception as e:
        return Response(status=500, data={'error': str(e)})


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        data = request.data if request.data is not None else {}
        required_fields = set(['username', 'password'])
        if not required_fields.issubset(data.keys()):
            return Response(status=400, data={'error': 'Missing required fields'})
        
        user = User.objects.get(username= data['username'])
        print((user))
        if user and pbkdf2_sha256.verify(data['password'], user.password):
            token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10)}, keys.JWT_SECRET)
            return Response(status=200, data={'token': token})
        else:
            return Response(status=401, data={'error': 'Invalid username or password'})

    except Exception as e:
        return Response(status=500, data={'error': str(e)})
    


@api_view(['PUT'])
@permission_classes([AllowAny])
def changePassword(request):
    try:
        data = request.data if request.data is not None else {}
        required_fields = set(['username', 'old_password', 'new_password'])
        if not required_fields.issubset(data.keys()):
            return Response(status=400, data={'error': 'Missing required fields'})
        user = User.objects.get(username= data['username'])
        if not user:
            return Response(status=404, data={'error': 'User not found'})
        if not pbkdf2_sha256.verify(data['old_password'], user.password):
            return Response(status=401, data={'error': 'Invalid old password'})
        new_password_hash = pbkdf2_sha256.hash(data['new_password'])
        user.password=new_password_hash
        user.save()
        return Response(status=200, data={'message': 'Password updated successfully'})
    except Exception as e:
        return Response(status=500, data={'error': str(e)})


