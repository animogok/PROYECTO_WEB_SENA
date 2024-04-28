from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'Login.html')

def register(request):
    return render(request, 'Register.html')
    
def home(request):
    
    return render(request, 'Home.html')