from django.shortcuts import render, redirect, HttpResponse
from .models import User, Umanager, Travel
from django.contrib import messages
def index(request):
    if 'id' in request.session:
        return redirect('/travels')
    return render(request, 'logReg/index.html')
def process(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        user_check = User.objects.reg(request.POST)
        print user_check
        if user_check['valid']:
            if 'id' not in request.session:
                new_user = User.objects.filter(email=request.POST['email'])[0]
                request.session['id'] = new_user.id
                messages.add_message(request, messages.INFO, 'Registration is successful')
                return redirect('/travels')
        else:
            err_msg = user_check['msg']
            for val in err_msg:
                messages.add_message(request, messages.INFO, val)
            return redirect('/')
def log_in(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        user_log = User.objects.log(request.POST)
        if user_log['valid']:
            if 'id' not in request.session:
                logged = User.objects.filter(email=request.POST['elog'])[0]
                request.session['id'] = logged.id
                return redirect('/travels')
        else:
            log_err = user_log['msg']
            for val in log_err:
                messages.add_message(request, messages.INFO, val)
            return redirect('/')


def travels(request):
    if 'id' not in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in")
        return redirect('/')
    else:
        travel = Travel.objects.all()
        user = User.objects.get(id=request.session['id'])
        context = {
            'others': User.objects.exclude(id=request.session['id']),
            'users': user,
            'trips': travel,
        }
        return render(request, 'logReg/travels.html', context)


def destination(request, id):
    context = {
        'trips'
        'trip_id': Travel.objects.get(id=id),
        'users': User.objects.get(id=request.session['id']),
    }


    return render(request, 'logReg/destination.html', context)


def add(request):
    if request.method == 'GET':
        return render(request, 'logReg/add.html')


def proc_add(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        Travel.objects.create(destination=request.POST['dest'], description=request.POST['desc'], travel_start=request.POST['date_from'], travel_end=request.POST['date_to'], user=user)
        Travel.objects.add_trip(request.POST)
        return redirect('/travels')


def log_out(request):
    request.session.flush()
    return redirect('/')
def error(request):
    messages.add_message(request, messages.INFO, "Page does not exist")
    return redirect('/')
