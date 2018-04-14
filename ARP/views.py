from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics, parsers, renderers
from .models import (
    ARPUser, Infection
)
from .serializers import (
    UserCreateSerializer,
    ARPUserSerializer,
    AuthTokenSerializer,
    InfectionSerializer,
)


# Create your views here.
class NewUser(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = (parsers.JSONParser, parsers.FormParser)
    # renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        user_data = ARPUserSerializer(user, context={'request': request}).data
        user_data['token'] = token.key
        return Response(user_data, status=status.HTTP_202_ACCEPTED)


class Logout(APIView):
    @staticmethod
    def get(request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)


class SubmitInfectionData(APIView):
    @staticmethod
    def post(request):
        serializer = InfectionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            infection = serializer.save()
            infection.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


