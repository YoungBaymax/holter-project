# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    kwargs = {'title': 'Holter Monitor Web'}
    return render(request, 'base.html', kwargs)
