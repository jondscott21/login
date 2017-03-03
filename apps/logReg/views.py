from django.shortcuts import render, redirect, HttpResponse
from django.db.models import F, Count
from .models import User, Umanager, Quote, AddQuote, Favorite
from django.contrib import messages
def index(request):
    if 'id' in request.session:
        return redirect('/quotes')
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
                return redirect('/quotes')
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
                return redirect('/quotes')
        else:
            log_err = user_log['msg']
            for val in log_err:
                messages.add_message(request, messages.INFO, val)
            return redirect('/')


def quotes(request):
    if 'id' not in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['id'])
        quotes = Quote.objects.exclude(quote_fav__fav_user=user)
        favs = Quote.objects.filter(quote_fav__fav_user=user)
        context = {
            'quotes': quotes,
            'user': user,
            'favs': favs,
        }
        return render(request, 'logReg/quotes.html', context)


def addquote(request):
        if request.method == 'GET':
            return redirect('/')
        elif request.method == 'POST':
            user = User.objects.get(id=request.session['id'])
            addquote = AddQuote()
            addquote.add_quote(request.POST, user)
            if addquote.is_valid:
                return redirect('/quotes')
            else:
                for val in addquote.quote_errors:
                    messages.add_message(request, messages.INFO, val)
                return redirect('/quotes')


def add_fav(request, id):
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        user = request.session['id']
        quote = Quote.objects.get(id=id)
        # if Favorite.objects.filter(fav_user_id=user, fav_quote_id=id).exists():
        Favorite.objects.create(fav_user_id=user, fav_quote_id=id)

        return redirect('/quotes')


def rem_fav(request, id):
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        Favorite.objects.filter(fav_user_id=user, fav_quote_id=id).delete()
        return redirect('/quotes')


def users(request, id):
    user = User.objects.get(id=id)
    quotes = Quote.objects.filter(poster=user)
    count = quotes.exclude(poster=user).count()
    context = {
        'user': user,
        'quotes': quotes,
        'count': count
    }
    return render(request, 'logReg/users.html', context)
def log_out(request):
    request.session.flush()
    return redirect('/')


def error(request):
    messages.add_message(request, messages.INFO, "Page does not exist")
    return redirect('/')
