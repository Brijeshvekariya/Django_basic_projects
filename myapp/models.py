from django.db import models

# Create your models here.
# class

class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30,unique=True)
    mobile=models.CharField(max_length=10)
    remarks=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    email=models.CharField(max_length=30,unique=True)
    mobile=models.CharField(max_length=10,unique=True)
    address=models.CharField(max_length=100)
    password=models.CharField(max_length=16)
    profile_pic=models.ImageField(upload_to='profile_pic/',default="")

    def __str__(self):
        return self.fname + " "+ self.lname