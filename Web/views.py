from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, 'Home.html')

def menu(request):
    return render(request,'Menu.html')

def booking(request):
    return render(request, 'Booking.html')