from django.shortcuts import render
from ..users.models import Message
from datetime import datetime as dt 

def index(request):
    secrets = Message.objects.all().order_by('-created_at')
    
    context = {
        'secrets': secrets
    }
    return render(request, 'sec/index.html', context)

def trending(request):
    secrets = Message.objects.all()
    secrets = sorted(secrets, key=lambda secret: -1*secret.n_likes) 
    
    context = {
        'secrets': secrets
    }
    return render(request, 'sec/trending.html', context)
