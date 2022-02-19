from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


from .models import MyUser
from .utils import send_activation_email


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
        send_activation_email(email=user.email, activation_code=user.activation_code)
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


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=60)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        MyUser = get_user_model()
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with given email does not exist')
        return email

    def validate_activation_code(self, activation_code):
        MyUser = get_user_model()
        if MyUser.objects.filter(activation_code=activation_code, is_active=False).exists():
            raise serializers.ValidationError('Wrong activation code')
        return activation_code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirm')
        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        activation_code = data.get('activation_code')
        password = data.get('password')

        try:
            MyUser = get_user_model()
            user = MyUser.objects.get(email=email, activation_code=activation_code)
        except:
            raise serializers.ValidationError('User not found')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user


# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#
#     def validate_email(self, email):
#         if not MyUser.objects.filter(email=email).exists():
#             raise serializers.ValidationError()
#         return email
#
#     def send_reset_email(self):
#         email = self.validated_data.get('email')
#         user = MyUser.objects.get(email=email)
#         user.create_activation_code()
#         message = f'Code for reset password {user.activation_code}'
#         send_mail(
#             'Reset password',
#             message,
#             'test@gmail.com',
#             [email, ]
#         )
#
#
# class CreateNewPasswordSerializer(serializers.Serializer):
#     activation_code = serializers.CharField(required=True)
#     password = serializers.CharField(min_length=6, required=True)
#     password_confirm = serializers.CharField(max_length=6, required=True)
#
#     def validate_activation_code(self, code):
#         if not MyUser.objects.filter(activation_code=code).exists():
#             raise serializers.ValidationError("don't right code")
#         return code
#
#     def validate(self, attrs):
#         password = attrs.get('password')
#         password_confirm = attrs.get('password_confirm')
#         if password != password_confirm:
#             raise serializers.ValidationError('passwords do not совпадают')
#         return attrs
#
#     def create_pass(self):
#         code = self.validated_data.get('activation_code')
#         password = self.validated_data.get('password')
#         user = MyUser.objects.get(activation_code=code)
#         user.set_password(password)
#         user.save()
#
#
# class ChangePasswordSerializer(serializers.Serializer):
#     old_pass = serializers.CharField(required=True)
#     new_pass = serializers.CharField(required=True, min_length=6)
#     new_pass_confirm = serializers.CharField(required=True, min_length=6)
#
#     def validate_old_pass(self, password):
#         request = self.context.get('request')
#         if not request.user.check_password(password):
#             raise serializers.ValidationError('enter do not right password')
#         return password
#
#     def validate(self, attrs):
#         pass_ = self.validated_data.get('new_pass')
#         pass_confirm = self.validated_data.get('new_pass_confirm')
#         if pass_ != pass_confirm:
#             raise serializers.ValidationError('неверное подтверждение нового пародля')
#         return attrs
#
#     def set_new_password(self):
#         request = self.context.get('request')
#         new_pass = self.validated_data.get('new_pass')
#         user = request.user
#         user.set_password(new_pass)
#         user.save()