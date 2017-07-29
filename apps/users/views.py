from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Message
from .models import Like
import logging
from django.http import JsonResponse

from dojosecrets.settings import SERVER_LOG

def is_logged_in(request):
    return request.session.get('logged_id', False)

def is_admin(request):
    # return request.session.get('is_admin', False)
    return False

def index(request):
    if is_logged_in(request):
        return redirect('sec:index')
    else:
        return redirect('logreg:login')

def show(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'users/show.html', {'user': user, 'is_admin': is_admin(request)})

def edit(request, user_id=None):
    print(SERVER_LOG)
    SERVER_LOG.debug('we find ourselves in the edit function')
    if request.method == 'GET':
        # show the edit page if it's a GET request
        if user_id:
            if not is_admin(request):
                return redirect('sec:index')
            
            user = User.objects.filter(id=user_id)
            if len(user) == 0:
                return redirect('sec:index')
            else:
                user = user[0]
        else:
            user = User.objects.get(id=request.session['user_id'])

        profile = user.id == request.session['user_id']
        context = {
            'user': user, 
            'is_admin': is_admin(request), # if theyre an admin, can change other's info
            'profile': profile # if theyre editing their own profile, then they can edit the description
            }
        return render(request, 'users/edit.html', context)

    elif request.method == 'POST':
        # posting to this route handles editing the user
        SERVER_LOG.debug('we got data!')
        SERVER_LOG.debug(request.POST)
        user = User.objects.filter(id=user_id)
        if len(user) == 0:
            return redirect('sec:index')
        user = user[0]
        
        if 'password' in request.POST:
            # editing password
            user.password_plaintext = request.POST['password']
            user, errors = user.edit_pw()

            if request.POST['password'] != request.POST['password2']:
                errors.append('Passwords do not match')

            if len(errors) == 0:
                user.encrypt_pw()
                user.save()
                messages.success(request, 'User password has been updated.')
        else:
            # editing non-password fields
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            # user.is_admin = bool(int(request.POST.get('is_admin', user.is_admin)))
            user.description = request.POST.get('description', user.description)
        
            user, errors = user.edit_info()        

            if len(errors) == 0:
                user.save()
                request.session['is_admin'] = user.is_admin
                
                
                messages.success(request, 'User info updated.')
        
        if len(errors) > 0:
            for err_msg in errors:
                messages.error(request, err_msg, extra_tags='danger')
        return redirect('users:edit', user_id)


def delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('sec:index')

def new(request):
    return render(request, 'users/new.html', {'is_admin': is_admin(request)})

def add_message(request):
    if request.method=='GET':
        return redirect('sec:index')

    from_user_id = request.session['user_id']
    
    content = request.POST['content']
    if len(content) > 0:
        new_message= Message.objects.create(
            from_user = User.objects.get(id=from_user_id),
            content = content
        )
    return redirect('sec:index')

def add_like(request, secret_id):
    
    from_user = User.objects.get(id=request.session['user_id'])
    print('new like by')
    print(from_user)
    secret = Message.objects.get(id=secret_id)
    newlike = Like.objects.create(
        from_user = from_user,
        message = secret
    )
    print(newlike)
    return JsonResponse({'response': "0"})