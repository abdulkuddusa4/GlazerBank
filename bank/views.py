from django.shortcuts import render,reverse
from django.contrib import messages
from django.http import FileResponse


def home(request):
    return render(request, 'index.html',)


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def contacts(request):
    return render(request, 'contact.html', {'contact': True})
