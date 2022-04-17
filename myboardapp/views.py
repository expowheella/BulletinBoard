from django.shortcuts import render
from django.http import HttpResponse
from .models import Bulletin


def home(request):
    context = {
        'bulletins': Bulletin.objects.all()
    }
    return render(request, 'myboardapp/home.html', context)

