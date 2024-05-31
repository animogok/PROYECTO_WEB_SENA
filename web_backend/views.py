from django.shortcuts import HttpResponseRedirect, render, redirect
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import Userserializer
import datetime

from web.views import home
from .forms import FormularioRegistrodeUsuarios, FormularioLogin
from .models import User_registrations

# Create your views here.

# POST method


class RegisterView(APIView):
    
    def get(self, request):
        form = FormularioRegistrodeUsuarios()
        return render(request, 'Register.html', {'form': form})

    def post(self, request):
        form = FormularioRegistrodeUsuarios(request.POST)
        serializer = Userserializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            user = User_registrations.objects.get(email = serializer.data['email'])
            user.set_password(serializer.data['password'])
            
            user.save()
            
            token = Token.objects.create(user = user)
            
            return Response({'token' : token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class Loginview(APIView):
    def get(self, request):
        form = FormularioLogin()
        return render(request, 'Login.html', {'form': FormularioLogin})

    def post(self, request):
        user = get_object_or_404(User_registrations, email=request.data['email'])
        
        if not user.check_password(request.data['password']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = Userserializer(instance=user)
        
        return Response({'token' : token.key, 'user': serializer.data}, status=status.HTTP_202_ACCEPTED)

# Metodo GET
class SettingsView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        token = request.GET.get('token')
        print(token)
        return render(request, 'Settings.html')
