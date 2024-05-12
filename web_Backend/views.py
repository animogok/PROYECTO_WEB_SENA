from django.shortcuts import render, redirect

from .forms import FormularioRegistrodeUsuarios
from .models import User_registrations

# Create your views here.

# POST method
def register(request):
    
    # We create the post method for the information the user should input in the form
    if request.method == "POST":
        form = FormularioRegistrodeUsuarios(request.POST)

        if form.is_valid():
            form.clean()
            form.save()
        else:
            form = FormularioRegistrodeUsuarios
    return render(request, 'Register.html', {'form': FormularioRegistrodeUsuarios })

# GET METHOD
async def login(request):
    
    if request.method == "POST":
        username = request.POST['formEmail']
        password = request.POST['formPassword']
    return render(request, 'Login.html')