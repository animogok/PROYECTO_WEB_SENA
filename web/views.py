from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'Home.html')
@login_required
def menu(request):
    return render(request,'Menu.html')
@login_required
def booking(request):
    return render(request, 'Booking.html')
