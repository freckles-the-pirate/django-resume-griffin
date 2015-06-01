from django.shortcuts import render
from griffin.models import *

def index(request):
    context = { '' : '' }
    return render(request, 'index.html', context)
