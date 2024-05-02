from django.shortcuts import render
from web_Backend.forms import FormularioRegistrodeUsuarios

# Create your views here.

def login(request):
    return render(request, 'Login.html')

def register(request):
    return render(request, 'Register.html', {'form' : FormularioRegistrodeUsuarios})
    
def home(request):
    return render(request, 'Home.html')

def menu(request):
    return render(request,'Menu.html')

def booking(request):
    return render(request, 'Booking.html')