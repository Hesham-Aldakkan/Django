from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from quest import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.


def home(request):
    return render(request, "webapp/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        password2 = request.POST.get('pass2')


        if User.objects.filter(username = username):
            messages.error(request, "Username already exists")
            return redirect("signup")

        if User.objects.filter(email = email):
            messages.error(request, "Email already exists")
            return redirect("signup")

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect("signup")
        
        if password != password2:
            messages.error(request, "Password didn't match")
        
        if not username.isalnum():
            messages.error(request, "Username must be alpha-Numeric")

        myuser = User.objects.create_user(username, email, password)

        myuser.save()



        #Welcome email

        subject = "Welcome to the Django app"
        message = "Hello " + myuser.username + ". Thank you for your interest in our app. \n " + " We have sent you a confirmation email please do confirm your email. \n" + "Regards. \n Hesham Aldakkan"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        messages.success(request, "Account has created successfully")

        return redirect('signin')

    return render(request, "webapp/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(request, username = username, password = pass1)

        if user is not None:
            login(request, user)
            userPage(request)
            return redirect('userPage')
        else:
            messages.error(request, "Not found")
            return redirect('signin')

    return render(request, "webapp/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "signed out")
    return redirect('home')


def userPage(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "logged out successfully")

    return render(request, "webapp/userPage.html")