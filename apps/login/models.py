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
        if len(data['first_name']) < 2:
            e['first_name'] = "first name must be at least 2 characters"
        if len(data['last_name']) < 2:
            e['last_name'] = "last name must be at least 2 characters"
        if not EMAIL_REGEX.match(data['email']):
            e['email'] = "email is invalid"
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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    pass_hash = models.CharField(max_length=255)
    objects = UserManager()