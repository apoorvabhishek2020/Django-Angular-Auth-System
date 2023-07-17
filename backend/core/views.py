from lib2to3.pgen2 import token
from rest_framework import exceptions
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from core.authentication import JWTAuthentication, create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from core.models import User, UserToken
import datetime

from core.serializers import UserSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException("Password don't match !")
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        UserToken.objects.create(
            user_id=user.id,
            token=refresh_token,
            expired_at=datetime.datetime.utcnow()+datetime.timedelta(days=7)
        )

        response = Response()

        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }


        return response


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        # auth = get_authorization_header(request).split()

        # if auth and len(auth)==2:
        #     token = auth[1].decode('utf-8')
        #     id = decode_access_token(token)
        #     user = User.objects.get(pk=id)
        #     if user:
        #         serializer = UserSerializer(user)
        #         return Response(serializer.data)
        # raise exceptions.AuthenticationFailed('Unauthenticated')
        return Response(UserSerializer(request.user).data)


class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        if not UserToken.objects.filter(
            user_id=id,
            token=refresh_token,
            expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).exists():
            raise exceptions.AuthenticationFailed("Unauthorized")

        access_token = create_access_token(id)

        return Response({
            'token': access_token
        })


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        UserToken.objects.filter(token=refresh_token).delete()
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message': 'success'
        }

        return response
