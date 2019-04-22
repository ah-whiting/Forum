from django.db import models
import re
import bcrypt
from django.db.models import Q

class UserManager(models.Manager):
    def validator(self, data):
        e = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}$')
        # Password matching expression. Password must be at least 4 characters, no more than 8 characters, and must include at least one upper case letter, one lower case letter, and one numeric digit.
        if len(data['username']) < 2 or len(data['username']) > 45:
            e['username'] = "user name must be between 2 and 45 characters"
        elif len(self.filter(username = data['username'])) > 0:
            e['username'] = "that username is taken"
        if not EMAIL_REGEX.match(data['email']):
            e['email'] = "email is invalid"
        elif len(self.filter(email = data['email'])) > 0:
            e['email'] = "there is already an account with that email address"
        # if not PASSWORD_REGEX.match(data['password']):
        #     e['password'] = 'Password must contain at least 1 lowercase letter, 1 uppercase letter, and one number'
        if data['password'] != data['c_password']:
            e['c_password'] = 'passwords must match'
        return e

    def login_validator(self, data):
        e = {}
        if len(data['email']) < 2 or len(data['password']) < 2:
            e['login'] = "login field must be completed"
            return e
        user = User.objects.filter(email = data['email'])
        if len(user) == 0 or not bcrypt.checkpw(data['password'].encode(),user[0].pass_hash.encode()):
            e['login_check'] = "invalid login"
        return e
            
class User(models.Model):
    username = models.CharField(max_length=45)
    email = models.EmailField(max_length=254)
    pass_hash = models.CharField(max_length=255)
    objects = UserManager()