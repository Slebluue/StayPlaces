from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime

class UserManager(models.Manager):
    #REGISTER VALIDATION
    def register_validator(self, postData):
        errors = []

        #Post data variables
        first_name = postData['first_name']
        last_name = postData['last_name']
        username = postData['username']
        date = postData['date']
        email = postData['email'].lower()
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        password = postData['password']
        confirm = postData['confirm-password']

        #Basic validations for register
        if len(email) < 1 or len(first_name) < 1 or len(last_name) < 1 or len(password) < 1 or len(confirm) < 1:
            errors.append('Please fill out all fields')
        if any(char.isdigit() for char in first_name) or any(char.isdigit() for char in last_name):
            errors.append('No numbers in name fields')
        if len(password) < 8 or len(confirm) < 8:
            errors.append('Password needs to be more than 8 characters')
        if password != confirm:
            errors.append('Passwords need to match')
        if match == None:
            errors.append('Email is not valid!')

        #Checking if email/username are already taken
        if len(self.filter(username=username)) > 0:
            errors.append('Username already taken')
        if len(self.filter(email=email)) > 0:
            errors.append('email already taken')

        if len(errors):
            return (False, errors)
        else:
            #Success set hashed pw and create new user
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.create(first_name=first_name, last_name=last_name,email=email, birthday= date, username=username, password=hashed)
            user = self.get(email=email)
            return (True, user)

    def edit_validator(self, postData, fileData, user):
        errors = []

        #Post data variables
        first_name = postData['first_name']
        last_name = postData['last_name']
        email = postData['email'].lower()
        location = postData['location']
        desc = postData['desc']
        gender = postData['gender']
        phone = postData['phone']
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

        try:
            image = fileData['image']
        except:
            if user.image:
                image = user.image
            else:
                image = None

        #Basic validations for register
        if len(email) < 1 or len(first_name) < 1 or len(last_name) < 1:
            errors.append('Please fill out all fields')
        if any(char.isdigit() for char in first_name) or any(char.isdigit() for char in last_name):
            errors.append('No numbers in name fields')
        if match == None:
            errors.append('Email is not valid!')

        #Checking if email is already taken
        if len(self.filter(email=email)) > 0 and email != user.email:
            errors.append('email already taken')

        if len(errors):
            return (False, errors)
        else:
            #Success and edit new user
            user = self.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.image = image
            user.location = location
            user.phone = phone
            user.desc = desc
            user.gender = gender
            user.save()
            return (True, user)

    # LOGIN VALIDATION
    def login_validator(self, postData):
        errors = []

        #Post Data variables
        username = postData['username']
        password = postData['password']

        #Check if username is valid, if it is grab the stored pw also
        try:
            user = self.get(username=username)
            stored_hashed = user.password  
        except:
            errors.append('Invalid Username')
            return (False, errors)
        
        #check if password matches
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed.encode('utf-8')):
            errors.append('Incorrect Password')
        
        if len(errors):
            return (False, errors)
        else:
            user = self.get(username=username)
            return (True, user)

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    desc = models.CharField(max_length=500, blank=True, null=True)
    birthday = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    image = models.FileField(upload_to='media/%Y/%m/%d',null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    #Add UserManager functionality to user.objects
    objects = UserManager()

class Host(models.Model):
    user = models.OneToOneField(User, related_name="host")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Host_Review(models.Model):
    content = models.CharField(max_length=255)
    rating = models.IntegerField(blank=True, null=True)
    host = models.ForeignKey(Host,related_name="reviews")
    rated_by = models.ForeignKey(User,related_name="host_reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

