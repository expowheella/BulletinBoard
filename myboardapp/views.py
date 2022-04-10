from django.shortcuts import render
from django.http import HttpResponse
from .models import Bulletin

bulletins = [
    {
        'title': 'Snikers',
        'name': 'Reebok',
        'cost': 100,
        'date_posted':'10.10.2020'
    },
    {
        'title': 'Snikers',
        'name': 'Puma',
        'cost': 90,
        'date_posted':'12.11.2020'
    }
]

def home(request):
    context = {
        'bulletins': bulletins
    }
    return render(request, 'myboardapp/home.html',context)

