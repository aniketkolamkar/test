from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
# from .models.customer import Customer
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User, GroupManager
import requests
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
import json
from .tokens import account_activation_token
from django.contrib.contenttypes.models import ContentType
import datetime
from datetime import timedelta
from django.contrib import messages

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name','groups')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        user.set_password(validated_data['password'])
        user.is_active = False # Deactivate account till it is confirmed
        user.groups.set(groups_data)
        user.save()
        
        request = self.context.get('request')
        current_site = get_current_site(request)

        url = "https://api.sendinblue.com/v3/smtp/email"

        payload = json.dumps({
        "sender": {
            "name": "6Simplex",
            "email": "butler@6simplex.co.in"
        },
        "to": [
            {
            "email": validated_data.get('email'),
            "name": validated_data.get('first_name+last_name')
            }
        ],
        "subject": "Verification Link",
        "textContent": render_to_string('emails/account_activation_email.html', {'user': user,'domain': current_site.domain,'uid': urlsafe_base64_encode(force_bytes(user.pk)),'token': account_activation_token.make_token(user),})
        })
        headers = {
            'accept': 'application/json',
            'api-key': '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',
            'content-type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

        first_name = validated_data['first_name']
        last_name = validated_data['last_name']


        user_name = first_name + last_name
        message = {
            "username": validated_data['username'],
            "email": validated_data['email'],
            "first_name":validated_data['first_name'],
            "last_name":validated_data['last_name'],
            "groups": groups_data,
            "message": f"{user_name} Please Verify Your Email ID"
                }

        return message
        
    def Destroy(self, username):
        user = User.objects.delete(username=username)
        # customer = Customer.objects.delete(username=username)
        user.save()
        # customer.save()

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UpdateUserSerializer(serializers.Serializer):
    model = User

    """
    Serializer for Update User change endpoint.
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def update(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.save()


class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name','permissions')


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        # pass
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


