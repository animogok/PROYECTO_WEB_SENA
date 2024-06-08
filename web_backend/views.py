from django.core.cache import cache
from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login,logout, authenticate
from django.conf import settings

import jwt

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import Userserializer

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
    
            Token.objects.create(user = user)
            
            return Response({"user" : serializer.data}, status=status.HTTP_201_CREATED)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Loginview(APIView):
    success_url = reverse_lazy("home")
    
    def get(self, request):
        form = FormularioLogin()
        return render(request, 'Login.html', {'form': form})
        
    def post(self, request):
        user = get_object_or_404(User_registrations, email = self.request.data['email'])
        
        if not user.check_password(self.request.data['password']):
            return Response({"error": "incorrect password"},status=status.HTTP_401_UNAUTHORIZED)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = Userserializer(instance=user)
        login(request, token.user)
        self.request.session.set_expiry(600)
        
        return Response({"token" : token.key, "user":serializer.data}, status=status.HTTP_202_ACCEPTED)
    


class AccountSettings(APIView):
    
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'Settings.html', {"user": self.request.user})
    
    def post(self, request):
        user = get_object_or_404(User_registrations, email = self.request.user)
        
        if 'change_password' in self.request.POST:
            if user.check_password(self.request.POST['actual_pass']):
                if self.request.POST['new_pass'] == self.request.POST['confirm_pass']:
                    user.set_password(self.request.POST['new_pass'])
                    user.save()
                    return Response({"username" : user.email, "change":"Your password change was succesfull"}, status=status.HTTP_202_ACCEPTED)
                else:
                     return Response({"error" : "Password mismatch"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : "Password incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            pass
        
        if 'change_email' in self.request.POST:
            email = request.POST['new_email']
            user.email = email    
            user.save()
            return Response({"username" : user.email, "change":"Your email change was succesfull"}, status=status.HTTP_202_ACCEPTED)
        

def logout_app(request):
    logout(request)
    return redirect("home")