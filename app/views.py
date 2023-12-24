from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import *
from django.contrib.auth import login,logout,authenticate
from .models import *
from rest_framework.parsers import MultiPartParser,FormParser
from .authenticate import SessionCsrfExemptAuthentication
from rest_framework.authtoken.models import Token

# Create your views here.

class AuthenticateUser(APIView):
    def get(self,request):
        return Response('Text')


class CreateUser(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        return Response({'detail':'register user'})
    def post(self,request):
        if User.objects.filter(email=request.data['email']).first() is not None:
            return Response({"error":"Email already used"}, status=400)
        serializer=CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            token=serializer.create(serializer.validated_data)
        return Response({"user":token},status=200)

class Login(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        return Response({"user":"user"})
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.check_password(serializer.validated_data)
            if user is not None:
                token=Token.objects.get(user=user)
                return Response({"user":token.key,"id":user.id})
            else:
                return Response({"error":"Invalid login credentials"},status=400)
        return Response({"invalid":"login failed"},status=403   )

class GetUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        user_serializer=UserSerializer(user)
        return Response({"user":user_serializer.data})



class GetProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        serializer=ProfileSerializer(Profile.objects.get(user=user))
        return Response({"profile":serializer.data})

    def patch(self,request):
        profile_obj=Profile.objects.get(user=request.user)
        serializer=ProfileSerializer(profile_obj,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        logout(request)
        return Response({"message":"logout successful"})

class CreateInvestment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser,FormParser]
    def get(self,request):
        if(len(Investments.objects.filter(user=request.user))==0):
            return Response({"investments":[]})
        serializer=InvestmentSerializer(Investments.objects.filter(user=request.user).order_by('-id'),many=True)
        return Response({"investments":serializer.data})

    def post(self,request,format=None):
        serializer=InvestmentSerializer(data=request.data)
        Investments.objects.create(
            user=request.user,
            amount=int(request.data['amount']),
            inv_type=request.data['inv_type'],
            frequency_type=request.data['frequency_type'],
            image=request.data["image"],
            confirmed=False

        )
        if serializer.is_valid():
            serializer.save()
            return Response({"investment":"created"},status=200)
        return Response({"success":"custom create"},status=200)
