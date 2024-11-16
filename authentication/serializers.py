from rest_framework import serializers
from rest_framework.validators import ValidationError
from authentication.models import User
from rest_framework.authtoken.models import Token

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=20)
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(min_length=6, write_only=True)
    

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        username_exists = User.objects.filter(username=attrs['username']).exists()
        phone_number_exists = User.objects.filter(phone_number=attrs['phone_number']).exists()

        if email_exists:
            raise ValidationError('Email already exists')
        if username_exists:
            raise ValidationError('Username already taken')
        if phone_number_exists:
            raise ValidationError('This phone number is already associated with an existing account')    

        return super().validate(attrs)


    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'password']
        # extra_kwargs = {'password' : {'write_only': True}}


    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        Token.objects.create(user=user)

        user.save()

        return user


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

#Serializer for handling password change/update

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    confirm_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)