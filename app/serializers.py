from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','first_name','last_name','password']

    def create(self,data):
        if self.check_email_unique(data['email']):
            raise serializers.ValidationError(detail={"message":"Email already used"},code=403)
        new_user=User.objects.create(
            username=data['email'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        new_user.set_password(data['password'])
        new_user.save()
        Profile.objects.create(
            user=new_user
        )
        return new_user

    def check_email_unique(self,email):
        if User.objects.filter(email=email).first() is not None:
            return True
        else:
            return False

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','first_name','last_name',]


class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Profile
        fields='__all__'


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

    def check_password(self,data):
        user=User.objects.filter(email=data['email']).first()
        if user is None:
            raise serializers.ValidationError(detail={"message":"No account with email found"},code=403)
        else:
            auth=authenticate(username=user.username,password=data['password'])
            return auth

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Investments
        fields="__all__"

