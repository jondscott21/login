from django.shortcuts import render, redirect, HttpResponse
from django.db.models import F
from .models import User, Umanager, Poke
from django.contrib import messages
def index(request):
    if 'id' in request.session:
        return redirect('/pokes')
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
                return redirect('/pokes')
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
                return redirect('/pokes')
        else:
            log_err = user_log['msg']
            for val in log_err:
                messages.add_message(request, messages.INFO, val)
            return redirect('/')


def pokes(request):
    if 'id' not in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in")
        return redirect('/')
    else:
        peoples = User.objects.all().exclude(id=request.session['id'])
        pokes = Poke.objects.all()
        user = User.objects.get(id=request.session['id'])
        pokes = Poke.objects.get(poke_count=peoples)
        context = {
            'peoples': peoples,
            'user': user,
            'pokes': pokes
        }
        return render(request, 'logReg/templates/logReg/pokes.html', context)


def add_poke(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        if Poke.objects.filter(poker_id=user.id, pokee_id=id).exists():
            counter = Poke.objects.get(poker_id=user.id, pokee_id=id)
            counter.poke_count = F('poke_count') + 1
            counter.save()
            return redirect('/pokes')
        else:
            Poke.objects.create(poker_id=user.id, poke_count=1, pokee_id=id)
        return redirect('/pokes')


def log_out(request):
    request.session.flush()
    return redirect('/')


def error(request):
    messages.add_message(request, messages.INFO, "Page does not exist")
    return redirect('/')
