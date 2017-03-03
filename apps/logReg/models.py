from __future__ import unicode_literals
from django.forms import extras
from django.db import models
from time import time, strftime, localtime
from datetime import datetime
import re, bcrypt
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
PASSWORD_REGEX = re.compile(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})', re.MULTILINE)
name_regex = re.compile(r'[a-zA-Z]{3,}$', re.MULTILINE)

# Create your models here.
class Umanager(models.Manager):
    def reg(self, postData):
        status = {}
        msg = []
        name = postData['name']
        alias = postData['alias']
        email = postData['email']
        password = postData['password']
        confirm = postData['confirm']
        bday = postData['bday']
        if len(name) < 3 or len(alias) < 3:
            msg.append("Name fields cannot be blank, and must contain least 3 letters")
        elif not name_regex.match(name):
            msg.append("Name field can only contain letters")
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
            msg.append('Invalid birthday format. Format should be mm/dd/yyyy.')
        elif bday > strftime('%Y-%m-%d'):
            msg.append("That date hasn't happened yet")
        if not msg:
            valid = True
            pwhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(name=name, alias=alias, email=email, password=pwhash, bday=bday)
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


class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bday = models.DateTimeField(auto_now=False, auto_now_add=False)
    objects = Umanager()


class Quote(models.Model):
    quote = models.TextField(max_length=100)
    author = models.CharField(max_length=45)
    poster = models.ForeignKey(User, related_name='who_post')


class Favorite(models.Model):
    fav_user = models.ForeignKey(User, related_name='user_fav', null=True, blank=True)
    fav_quote = models.ForeignKey(Quote, related_name='quote_fav', null=True, blank=True)


class AddQuote(object):
    def __init__(self):
        self.quote_errors = []
        self.is_valid = True

    def validate_quote(self, data):
        if len(data['author']) < 4 and len(data['quote']) < 11:
            self.quote_errors.append("Authors must be at least 3 characters")
            self.quote_errors.append("You have at least 10 characters per quote")
            self.is_valid = False
        elif len(data['author']) < 4:
            self.quote_errors.append("Authors must be at least 3 characters")
            self.is_valid = False
        elif len(data['quote']) < 11:
            self.quote_errors.append("You have at least 10 characters per quote")
            self.is_valid = False

    def add_quote(self, data, user):
        self.validate_quote(data)
        if self.is_valid:
            Quote.objects.create(quote=data['quote'], author=data['author'], poster=user)