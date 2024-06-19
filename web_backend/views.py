from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
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
    
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        form = FormularioRegistrodeUsuarios()
        return render(request, 'Register.html', {'form': form})
    
    @method_decorator(csrf_protect)
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        form = FormularioRegistrodeUsuarios(request.POST)

        if form.is_valid():
            serializer = Userserializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = User_registrations.objects.get(email = serializer.data['email'])
                user.set_password(serializer.data['password'])
                user.save()
        
                Token.objects.create(user = user)
                
                return redirect("login")
            
            else:
                return render(request, 'Register.html', {'form': form,
                                                        "error" : True
                                                        })
                
        return render(request, 'Register.html', {'form': form,
                                                        "error" : True
                                                        })

class Loginview(APIView):
    success_url = reverse_lazy("home")
    form = FormularioLogin()
    
    @method_decorator(csrf_protect, ensure_csrf_cookie)
    def get(self, request):
        return render(request, 'Login.html', {'form': self.form})
    
    @method_decorator(csrf_protect, ensure_csrf_cookie)
    def post(self, request):
        user = get_object_or_404(User_registrations, email = self.request.data['email'])
        
        if not user.check_password(self.request.data['password']):
            return render(request, 'Login.html', {'form': self.form,
                                                  "error" : True
                                                  })
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = Userserializer(instance=user)
        login(request, token.user)
        self.request.session.set_expiry(600)
        self.request.session['user_token'] = token.key
        
        return HttpResponseRedirect(self.success_url)
    
class AccountSettings(APIView):
    
    @method_decorator(login_required)
    @method_decorator(csrf_protect, ensure_csrf_cookie)
    def get(self, request):
        return render(request, 'Settings.html', {"user": self.request.user})
    
    @method_decorator(csrf_protect, ensure_csrf_cookie)
    def post(self, request):
        user = get_object_or_404(User_registrations, email = self.request.user)
        
        if 'change_password' in self.request.POST:
            if user.check_password(self.request.POST['actual_pass']):
                if self.request.POST['new_pass'] == self.request.POST['confirm_pass']:
                    user.set_password(self.request.POST['new_pass'])
                    user.save()
                    
                    return render(request, 'Settings.html', {"user": self.request.user,
                                                             "success" : True
                                                             })
                else:
                     return render(request, 'Settings.html', {"user": self.request.user,
                                                             "error_1" : True
                                                             })
            else:
                return render(request, 'Settings.html', {"user": self.request.user,
                                                             "error_2" : True
                                                             })
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