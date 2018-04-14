from rest_framework import serializers
from .models import ARPUser, Infection, Message
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARPUser
        fields = [
            'username',
            'employee_id',
            'email',
            'phone',
            'machine_status',
        ]


class ARPUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ARPUser
        fields = [
            'employee_id',
            'username',
            'email',
            'phone',
        ]


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username")
    password = serializers.CharField(label="Password", style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            raise AuthenticationFailed
        attrs['user'] = user
        return attrs


class InfectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infection
        exclude = ('id',)


class UserInfectionSerializer(serializers.ModelSerializer):
    infections = serializers.SerializerMethodField()

    def get_infections(self, obj):
        infections = Infection.objects.filter(victim_employee=obj)
        if infections.exists():
            return InfectionSerializer(infections, many=True).data
        else:
            return []

    class Meta:
        model = ARPUser
        fields = [
            'employee_id',
            'infections',
        ]


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        exclude = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):
    infections = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    def get_infections(self, obj):
        infections = Infection.objects.filter(victim_employee=obj)
        if infections.exists():
            return InfectionSerializer(infections, many=True).data
        else:
            return []

    def get_messages(self, obj):
        messages = Message.objects.filter(victim_id=obj)
        if messages.exists():
            return MessageSerializer(messages, many=True).data
        else:
            return []

    class Meta:
        model = ARPUser
        fields = [
            'username',
            'email',
            'phone',
            'machine_status',
            'infections',
            'messages',
        ]

