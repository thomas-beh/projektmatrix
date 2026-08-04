from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import random

def Projektmatrix(request):
    name = "Thomas"
    wochentag = datetime.now().strftime('%A')
    zahl = random.randint(1,100)
    return render(request, 'matrix.html', {'name': name, 'wochentag': wochentag, 'zahl': zahl})