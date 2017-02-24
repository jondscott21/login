from __future__ import unicode_literals
from django.forms import extras
from django.db import models
from time import time, strftime, localtime
import re, bcrypt
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
PASSWORD_REGEX = re.compile(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})', re.MULTILINE)
name_regex = re.compile(r'[a-zA-Z]{3,}$', re.MULTILINE)

# Create your models here.
class Umanager(models.Manager):
    def reg(self, postData):
        status = {}
        msg = []
        first = postData['first']
        last = postData['last']
        email = postData['email']
        password = postData['password']
        confirm = postData['confirm']
        bday = postData['bday']
        if len(first) < 3 or len(last) < 3:
            msg.append("Name fields cannot be blank, and must contain least 3 letters")
        elif not name_regex.match(first) or not name_regex.match(last):
            msg.append("Name fields can only contain letters")
        if len(email) < 1:
            msg.append("Email fields cannot be blank")
        elif len(User.objects.filter(email=email)) > 0:
            msg.append("Email address already taken")
        elif not EMAIL_REGEX.match(email):
            msg.append("Invalid email format")
        if len(password) < 1:
            msg.append("Password field cannot be blank")
        elif len(password) < 8:
            msg.append("Password must be at least 8 characters")
        elif not PASSWORD_REGEX.match(password):
            msg.append("Password must contain: 1 uppercase letter, 1 lowercase letter, and 1 number")
        if not password == confirm:
            msg.append('Must match password')
        if not re.search(r'^[0-9][0-9][0-9][0-9][\-][0-9][0-9][\-][0-9][0-9]', bday):
            msg.append('Invalid birthday format. Format should be dd/mm/yyyy.')
        elif bday > strftime('%d-%m-%Y'):
            msg.append("That date hasn't happened yet")
        if not msg:
            valid = True
            pwhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(first=first, last=last, email=email, password=pwhash, bday=bday)
        else:
            valid = False
        status.update({'valid': valid, 'msg': msg})

        return status

    def log(self, postData):
        status = {}
        msg = []
        email = postData['elog']
        password = postData['plog']
        if len(email) < 1 or len(password) < 1:
            msg.append("Login fields cannot be blank.")
        else:
            user_info = User.objects.filter(email=email)
            if not user_info:
                msg.append("Invalid user. Please Register")
            elif not bcrypt.checkpw(password.encode(), user_info[0].password.encode()):
                msg.append("Invalid password. Please Register")
        if not msg:
            valid = True
            status.update({'user_id': user_info[0].id})
        else:
            valid = False
            status.update({'msg': msg})
        status.update({'valid': valid})
        return status
    def add_trip(self, postData):
        dest = postData['dest']
        desc = postData['desc']
        fdate = postData['date_from']
        tdate = postData['date_to']
        return Travel.objects.create(destination=dest, description=desc, travel_start=fdate, travel_end=tdate)

class User(models.Model):
    first = models.CharField(max_length=45)
    last = models.CharField(max_length=45)
    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bday = models.DateTimeField(auto_now=False, auto_now_add=False, default="9999-11-29")
    objects = Umanager()

class Travel(models.Model):
    destination = models.CharField(max_length=45, null=True, blank=True)
    plan = models.ManyToManyField(User, related_name='user_plan')
    user = models.ForeignKey(User, related_name='travel', blank=True, null=True)
    description = models.CharField(max_length=45, null=True, blank=True)
    travel_start = models.DateTimeField(auto_now=False, auto_now_add=False, default='9999-11-29', null=True, blank=True)
    travel_end = models.DateTimeField(auto_now=False, auto_now_add=False, default='9999-11-29', null=True, blank=True)
    objects = Umanager()