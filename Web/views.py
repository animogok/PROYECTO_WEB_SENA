from django.shortcuts import render
from web_Backend.forms import FormularioRegistrodeUsuarios

# Create your views here.

def login(request):
    return render(request, 'Login.html')

def register(request):
    return render(request, 'Register.html', {'form' : FormularioRegistrodeUsuarios})
    
def home(request):
    return render(request, 'Home.html')