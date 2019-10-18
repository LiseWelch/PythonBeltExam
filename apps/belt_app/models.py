from django.db import models
from datetime import datetime, date
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user = User.objects.filter(email=postData['email'])
        if len(user) != 0:
            errors['not_unique'] = "User with this e-mail already exist"
            return errors
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name needs to be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name needs to be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = ("Invalid e-mail address")
        if len(postData['password']) < 8:
            errors["password"] = "Password needs to be at least 8 characters long"
        if postData['password']!=postData['confirm']:
            errors["confirm"] = "Passwords do not match"
        return errors

class ApptManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        cur_date = datetime.now()
        rel_date = datetime.strptime(postData['date'], '%Y-%m-%d')
        if len(postData['task']) < 5:
            errors['task'] = "Task must be at least 5 characters long"
        else:
            if (postData['status'] == 'Pending') & (rel_date<cur_date):
                errors['status'] = "Date must be in the future for pending tasks"
            if (postData['status'] == 'Missed') & (rel_date>cur_date):
                errors['status'] = "Date must be in the past for missed tasks"
            if (postData['status'] == 'Done') & (rel_date>cur_date):
                errors['status'] = "Date must be in the past for completed tasks"
        return errors
        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Appt(models.Model):
    task = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=10)
    user = models.ForeignKey(User, related_name="appts")
    objects = ApptManager()

