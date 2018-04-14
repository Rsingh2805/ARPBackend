from rest_framework import serializers
from .models import ARPUser, Infection
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
        fields = '__all__'


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


class UserProfileSerializer(serializers.ModelSerializer):
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
            'username',
            'email',
            'phone',
            'machine_status',
            'infections',
        ]