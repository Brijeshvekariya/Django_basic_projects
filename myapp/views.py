from django.shortcuts import render
from . models import Contact,User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    if request.method=="POST":
        Contact.objects.create (
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            remarks = request.POST['remarks']
        )
        msg=" Message Send Successfully"
        contacts = Contact.objects.all().order_by('-id')[:3]
        return render(request,'contact.html',{'msg':msg, 'contacts':contacts},)
    else: 
        contacts= Contact.objects.all().order_by('-id')
        return render(request, 'contact.html',{'contacts':contacts})
def login(request):
    if request.method=="POST":
        try:
            user= User.objects.get(
                email=request.POST['email'],
                password=request.POST['password']
                )
            request.session['email']=user.email
            request.session['fname']=user.fname
            msg1=" Login Succesfully"
            return render(request,'home.html',{'msg1':msg1})           
        except User.DoesNotExist:
            msg=" Email or Password is Incorrect! Try Again"
            return render(request, 'login.html',{'msg':msg})
    else:
        return render(request, 'login.html',)

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg=" Email Already Registered!"
            return render(request, 'signup.html', {'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                )
                msg1=" Sign Up Successfully!"
                return render(request,'login.html',{'msg1':msg1})
            else:
                msg=" Password Does Not Match!"
                return render(request, 'signup.html', {'msg':msg})
    else:
        return render(request, 'signup.html')
    
def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        msg2 = " Logout Successfully ! "
        return render(request,'login.html',{'msg2':msg2})  # Redirect to the 'login' URL name
    # return render(request,'login.html',{'msg2':msg2})
    except:
        pass

# how to solve this error of changing password
def change_password(request):
    if request.method=='POST': 
        user=User.objects.get(email= request.session['email'])
        if user.password==request.POST['password']:
            if request.POST['npassword']==request.POST['cnpassword']:
                user.password=request.POST['npassword']
                user.save()
                msg1 = " Password Updated Succesfully"
                return render(request,'login.html',{'msg1':msg1})
            else:
                msg = " New Password and Confirm Password doesnot match"
                return render(request,'change_password.html',{'msg':msg})
        else:
            msg = " Passwords do not match"
            return render(request,'change_password.html',{'msg':msg})
    else:
        return render(request,'change_password.html')

def forgot_password(request):
    if request.method=='POST':
        try:
            user = User.objects.get(email= request.POST['email'])
            otp = random.randint(1000,9999)
            subject = 'OTP for Forgot Password'
            message = f'Hi {user.fname}, OTP is {str(otp)}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'otp.html',{'email':user.email,'otp':otp})
        except User.DoesNotExist:
            msg=" Email not Registered"
            return render(request,'forgot_password.html',{'msg':msg})
    else:
        return render(request,'forgot_password.html')

def verify_otp(request):
        email = request.POST['email']
        otp = request.POST['otp']
        votp = request.POST['votp']
        if otp == votp:
            return render(request,'new_password.html',{'email':email})
        else:
            msg = " Incorrect OTP"
            return render(request,'otp.html',{'email':email,'msg':msg})
        
def new_password(request):
    email = request.POST['email']
    npass = request.POST['npassword']
    cnpass = request.POST['cnpassword']
    try:
        if npass==cnpass:
            user= User.objects.get(email=email)
            user.password=npass
            user.save()
            msg1 = " Password Updated Succesfully"
            return render(request,'login.html',{'msg1':msg1})
        else:
            msg = " Passwords do not match"
            return render(request,'new_password.html',{'msg':msg})
    except User.DoesNotExist:
        msg = " User does not exist"
        return render(request,'new_password.html',{'msg':msg})