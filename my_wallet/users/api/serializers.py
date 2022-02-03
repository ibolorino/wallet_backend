from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as SimpleTokenObtainPairSerializer
from django.core.validators import validate_email


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



class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        
        if self.is_valid:
            email=self.validated_data['email']
            username=self.validated_data['username']
            user = User(username=username, email=email)
            password = self.validated_data['password']
            password2 = self.validated_data['password2']
            if password != password2:
                raise serializers.ValidationError({'password': ['As senhas devem ser iguais']})
            user.set_password(password)
            user.save()
            return user

    def validate_email(self, value):
        try:
            validate_email(value)
            return value
        except:
            raise serializers.ValidationError("Email inválido")
