from django.contrib.auth import authenticate
from rest_framework import serializers


from .models import MyUser
from .utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'phone_number', 'password', 'password_confirm', )

    def validate_phone_number(self, phone_number):
        if not phone_number.startswith('+996'):
            raise serializers.ValidationError('Use Kyrgyz numbers!')
        return phone_number

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return validated_data


    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
        phone_number = validated_data.get('phone_number')
        user = MyUser.objects.create_user(email=email, username=username, password=password, phone_number=phone_number)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user

#
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     username = serializers.CharField(max_length=155)
#     password = serializers.CharField(
#         label='Password',
#         style={'input_type': 'password'},
#         trim_whitespace=False
#     )
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         print(email)
#         print(attrs)
#         password = attrs.get('password')
#         username = attrs.get('username')
#         # phone_number = attrs.get('phone_number')
#
#         if email and password and username:
#             user = authenticate(request=self.context.get('request'), username=username, email=email, password=password)
#             print(user)
#             if not user:
#                 message = 'Unable to log in with provided credentials'
#                 raise serializers.ValidationError(message, code='authorization')
#         else:
#             message = 'Must include "email" and "password".'
#             raise serializers.ValidationError(message, code='authorization')
#
#         attrs['user'] = user
#         return attrs
