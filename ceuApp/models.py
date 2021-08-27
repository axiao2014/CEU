from django.db import models
from django.contrib import messages
from django.core.validators import validate_email
from datetime import date

# Create your models here.
class Course(models.Model):
    name=models.CharField(max_length=255)
    desc=models.TextField()
    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    unit=models.IntegerField()
    price=models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['username']) < 5:
            errors['username'] = "Username should be at least 5 characters."
        try:
            validate_email(post_data['email'])
        except:
            errors['email'] = "Please enter a valid email address."
        if len(post_data['password']) < 8:
            errors['password'] = 'Passwords should be at least 8 characters.'
        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = "Passwords do not match."
        if len(post_data['fname']) < 2 or not post_data['fname'].isalpha():
            errors['fname'] = "First name should be at least 2 characters; letters only."
        if len(post_data['lname']) < 2 or not post_data['lname'].isalpha():
            errors['lname'] = "Last name should be at least 2 characters; letters only."
        if post_data['ltype'] == '':
            errors['ltype'] = "Please select a license type."
        if post_data['lboard'] == '':
            errors['lboard'] = "Please select a license board."
        if len(post_data['lnum']) < 4:
            errors['lnum'] = "Please input a valid license number."
        return errors

class OrderManager(models.Manager):
    def basic_validator(self, post_data):
        errors={}
        if len(post_data['address']) == 0:
            errors['address'] = "Address cannot be blank."
        if len(post_data['zip_code']) >5:
            errors['address'] = "Zip code cannot be more than 5 characters."
        if len(post_data['zip_code']) <5:
            errors['address'] = "Zip code cannot be less than 5 characters."
        if len(post_data['city']) ==  0:
            errors['city'] = "City cannot be blank." 
        

class User(models.Model):
    admin=models.BooleanField(default=False)
    fname=models.CharField(max_length=40)
    lname=models.CharField(max_length=40)
    lnum=models.TextField()
    lexpire=models.DateField()
    ltype=models.TextField()
    lboard=models.TextField()
    email=models.EmailField()
    username=models.CharField(max_length=20)
    password=models.TextField()
    courses=models.ManyToManyField(Course, related_name='courses')
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    ord_dt=models.DateField()
    courses=models.ForeignKey(Course, related_name='ordered_courses',on_delete = models.CASCADE)
    user=models.ForeignKey(User, related_name='user',on_delete = models.CASCADE)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Billing(models.Model):
#     street=models.TextField()
#     street2=models.TextField()
#     city=models.TextField()
#     state=models.TextField(max_length=2)
#     zipcode=models.IntegerField(max_length=5)
#     user=models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)


