from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from user.models import User


class UserCreateSerializer(ModelSerializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError({"error": "User with this email already exists!"})

        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        name = "user"
        fields = ("first_name", "last_name", "email", "id", "password")
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }
