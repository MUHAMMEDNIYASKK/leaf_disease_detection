from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=15)
    utype = models.CharField(max_length=20)

class Hreg(models.Model):
    hname = models.CharField(max_length=50)
    build_no = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    img = models.FileField(upload_to='file')
    email = models.CharField(max_length=50)
    con = models.CharField(max_length=12)
    wname = models.CharField(max_length=20)
    rno = models.CharField(max_length=5)
    fno = models.CharField(max_length=6)
    rent = models.CharField(max_length=5)
    uname = models.CharField(max_length=20)
    type=models.CharField(max_length=15,default='BOYS')
    status = models.CharField(max_length=20)

class Sreg(models.Model):
    admnno = models.CharField(max_length=10)
    sfname =models.CharField(max_length=20)
    slname = models.CharField(max_length=20)
    stream = models.CharField(max_length=50)
    yoj = models.CharField(max_length=50)
    duration = models.CharField(max_length=10)
    semail = models.EmailField(max_length=50)
    con = models.CharField(max_length=12)
    housename = models.CharField(max_length=12)
    location = models.CharField(max_length=20)
    district = models.CharField(max_length=5)
    pin = models.CharField(max_length=6)
    pname = models.CharField(max_length=20)
    pemail = models.EmailField(max_length=20)
    img = models.FileField(upload_to='file')
    aadhar = models.FileField(upload_to='file')
    gender = models.CharField(max_length=20, default='')
    status = models.CharField(max_length=20)
    uname=models.CharField(max_length=20,default='')

class payment(models.Model):
    stid = models.CharField(max_length=6)
    htid = models.CharField(max_length=6)
    amt = models.CharField(max_length=10)
    accno = models.CharField(max_length=20)
    ifsc = models.CharField(max_length=20)
    date = models.DateField()

class room(models.Model):
    rno = models.CharField(max_length=6)
    stid = models.CharField(max_length=6)
    htid = models.CharField(max_length=6)




class feedback(models.Model):
    Hid = models.IntegerField(default=0)
    Sid = models.IntegerField(default=0)
    feedback = models.CharField(max_length=50,default='')
    date =models.CharField(max_length=50,default='')



