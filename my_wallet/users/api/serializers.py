from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as SimpleTokenObtainPairSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username",]

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }


class TokenObtainPairSerializer(SimpleTokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': {
            'autenticacao': ['Credenciais inválidas']
        }
    }