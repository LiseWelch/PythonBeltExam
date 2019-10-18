from django.shortcuts import render, redirect
from .models import User, Appt
from django.contrib import messages
from datetime import datetime, date
import bcrypt

def root(request) :
    if 'type' not in request.session:
        request.session['type'] = 'n'
    return render(request, 'belt_app/login.html')

def process(request) :
    if request.POST['type']=="register" :
        request.session['type'] = "r"
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items() :
                messages.error(request,value)
            return redirect('/')
        else :
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'],
                                last_name=request.POST['last_name'],
                                email=request.POST['email'],
                                password=pw_hash
            )
            user = User.objects.last()
            request.session['userid'] = user.id
            return redirect('/success')
    elif request.POST['type']=="login" :
        request.session['type'] = "l"
        user = User.objects.filter(email=request.POST['email'])
        if user :
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id 
                return redirect('/success')
            else:
                messages.warning(request,"Password is incorrect")
                return redirect('/')
        else:
            messages.warning(request,"User does not exit")
            return redirect('/')
    return redirect('/')

def success(request) :
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['userid'])
    }
    return render(request, 'belt_app/success.html', context)

def logout(request) :
    del request.session['userid']
    del request.session['type']
    return redirect('/')

def add_new(request) :
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        'cur_date': date.today()
    }
    return render(request, 'belt_app/new.html', context)

def create(request) :
    if 'userid' not in request.session:
        return redirect('/')
    errors = Appt.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items() :
            messages.error(request,value)
        return redirect('/appointments/add')
    else :
        user = User.objects.get(id=request.session['userid'])
        Appt.objects.create(task=request.POST['task'], date=request.POST['date'], status=request.POST['status'], user=user)
        return redirect('/appointments')

def all_appts(request) :
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'f_appts': [],
        'p_appts': []
    }
    cur_date = date.today()
    appts = context['user'].appts.all()
    for a in appts :
        if a.date >= cur_date :
            context['f_appts'].append(a)
        else :
            context['p_appts'].append(a)
    return render(request, 'belt_app/appt.html', context)

def update(request, id) :
    if 'userid' not in request.session:
        return redirect('/')
    errors = Appt.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items() :
            messages.error(request,value)
        return redirect(f"/appointments/{id}")
    appt = Appt.objects.get(id=id)
    appt.task = request.POST['task']
    appt.date = request.POST['date']
    appt.status = request.POST['status']
    appt.save()
    return redirect('/appointments')

def edit(request, id) :
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        'appt': Appt.objects.get(id=id)
    }
    return render(request, 'belt_app/edit.html', context)

def delete(request, id) :
    if 'userid' not in request.session:
        return redirect('/')
    appt = Appt.objects.get(id = id)
    appt.delete()
    return redirect('/appointments')

def catch(request) :
    if 'userid' not in request.session:
        return redirect('/')
    else:
        return redirect('/appointments')