from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics, parsers, renderers
from .models import (
    ARPUser, Infection, Message,
)
from .serializers import (
    UserCreateSerializer,
    ARPUserSerializer,
    AuthTokenSerializer,
    InfectionSerializer,
    UserProfileSerializer,
    UserInfectionSerializer,
    MessageSerializer,
)
from django.utils import timezone

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
            user = get_object_or_404(ARPUser, pk=request.data['victim_employee'])
            user.machine_status = 'INF'
            user.save()
            message = Message.objects.create(message_type='INF', victim_id=get_object_or_404(ARPUser, pk=request.data['victim_employee']), timestamp=request.data['timestamp'])
            message.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class GetInfectionHistory(APIView):
    @staticmethod
    def get(request):
        current_user = request.user
        if current_user.user_type == 'ADM':
            users = ARPUser.objects.all()
            serializer = UserInfectionSerializer(users, many=True)
        else:
            user = current_user
            serializer = UserInfectionSerializer(user, many=False)
        return Response(serializer.data)


class GetUserProfile(APIView):
    @staticmethod
    def get(request):
        current_user = request.user
        serializer = UserProfileSerializer(current_user, many=False)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        if request.user is None or request.user.user_type != 'ADM':
            return Response({"error": "You are not authorized to view this page"}, status=status.HTTP_401_UNAUTHORIZED)
        user = get_object_or_404(ARPUser, employee_id=request.data['employee_id'])
        serializer = UserProfileSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BreachFixed(APIView):

    @staticmethod
    def post(request):
        if request.user is None or request.user.user_type != 'ADM':
            return Response({"error": "You are not authorized to view this page"}, status=status.HTTP_401_UNAUTHORIZED)
        message = Message.objects.create(message_type='FIX', victim_id=request.data['victim_id'], timestamp=timezone.now())
        message.save()
        user = ARPUser.objects.get(pk=request.data['victim_id'])
        user.machine_status = 'SAF'
        user.save()
        return Response(MessageSerializer(message, many=False).data, status=status.HTTP_201_CREATED)
