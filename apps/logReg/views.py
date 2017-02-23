from django.shortcuts import render, redirect, HttpResponse
from .models import User, Umanager
from django.contrib import messages
def index(request):
    if 'id' in request.session:
        return redirect('/success')
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
                return redirect('/success')
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
                return redirect('/success')
        else:
            log_err = user_log['msg']
            for val in log_err:
                messages.add_message(request, messages.INFO, val)
            return redirect('/')
def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'users': User.objects.get(id=request.session['id'])
        }
        return render(request, 'logReg/success.html', context)
def log_out(request):
    del request.session['id']
    return redirect('/')