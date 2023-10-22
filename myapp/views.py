from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from . models import Contact,User
from django.contrib import messages

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
            return render(request,'index.html',)            # two diiferent mmsg not working
        except User.DoesNotExist:
            msg=" Email or Password is Incorrect! Try Again"
            return render(request, 'login.html',{'msg':msg})
    else:
         # Check for the "Log-out Successfully!" message in the session
        return render(request, 'login.html',)

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg1="Email Already Registered!"
            return render(request, 'signup.html', {'msg1':msg1})
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
                msg="Sign Up Successfully!"
                return render(request,'login.html',{'msg':msg})
            else:
                msg1="Password Does Not Match!"
                return render(request, 'signup.html', {'msg1':msg1})
    else:
        return render(request, 'signup.html')
    
def logout_view(request):
    logout(request)
    msg1 = "Logout Successfully ! "
    print(msg1)
    return redirect('login',{'msg1':msg1})  # Redirect to the 'login' URL name


def change_password(request):
    return render(request,'change_password.html')



