from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . models import Faculty, Department, Level, Course, Material, Year
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . token import generate_token




# Create your views here.
def home(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone')

        subject = "Thanks for contacting Student Hub"
        body = f"Hello {fname} {lname},\n\nThank you for reaching out to me, your message has been received successfully, we will get back to you in due time\n\nWarm Regards,\n\nOlajire Stephen\n"

        mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [email])
        mail.send()
        
        subject = "New message Alert"
        body = f"A new message was received from {fname} {lname} {phone}, with the message of '{message}', and a mail has been automatically sent to their email, which is {email} Please attend to it"
        
        mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [settings.EMAIL_HOST_USER])
        mail.send()
        messages.info(request, "Your message was sent successfully")
    return render(request, 'html/home.html')

def login(request):

    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')
        if username is None or password is None:
            messages.error(request, 'Email or password not found')
            return redirect('/login')
        
        User = auth.authenticate(username=username, password=password)
        if User is None:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
        auth.login(request, User)
        return redirect('dashboard')
    return render(request, 'html/login.html')

def signup(request):

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        if not username.isalnum:
            messages.error(request, "Username must be AlphaNumeric")
            return redirect("signup")
        email = request.POST.get('email')
        if User.objects.filter(username= username).exists():
            messages.error(request, "Username has already been used")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email has already been used")
            return redirect('signup')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password != cpassword:
            messages.info(request, "Passwords do not match")
            return redirect('signup')
        if not lastname or not firstname or not username or not email or not password:
            messages.info(request, "Incomplete details")
            return redirect ("signup")
        else:
            new_user = User.objects.create(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
            new_user.set_password(password)
            new_user.is_active = False
            new_user.save()

            # welcome email
            subject = 'Welcome to Student Hub'
            body = f"Hello {firstname} {lastname},\n\nThank you for using our platform, \n\n A confirmation mail will be sent to you shortly, pls confirm your email"
            mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [email])
            mail.send()

            #confirmation email
            current_site = get_current_site(request)
            email_subject = "Pls Confirm your Email"
            message = render_to_string ("email_confirmation.html", {
                'name': new_user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)), 
                'token': generate_token.make_token(new_user)
            })

            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [new_user.email]
            )
            email.fail_silently = True
            email.send()

            return redirect('/sending')

    return render(request, 'html/signup.html')

def sends(request):
    return render(request, 'html/sending.html')

@login_required(login_url='login')
def dashboard(request):
    faculties = Faculty.objects.all()
    context = {
        'faculties' : faculties
    }
    return render(request, 'html/dashboard.html', context)

def department(request, id):
    faculty = Faculty.objects.get(id = id)
    department = Department.objects.filter(faculty = faculty)
    context = {"department": department }
    return render(request, 'html/department.html', context)

def level(request, id):
    department = Department.objects.get(id = id)
    level = Level.objects.filter(department = department)
    context = {"level": level }
    return render(request, 'html/level.html', context)

def courses(request,id):
    level = Level.objects.get(id = id)
    course = Course.objects.filter(level = level)
    context = {"course": course }
    return render(request, 'html/courses.html', context)

def year(request,id):
    course = Course.objects.get(id = id)
    year = Year.objects.filter(course = course)
    context = {"year": year }
    return render(request, 'html/year.html', context)

def material(request,id):
    year = Year.objects.get(id = id)
    material = Material.objects.filter(year = year)
    context = {"material": material }
    return render(request, 'html/material.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')

def activate (request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        new_user = None
    
    if new_user is not None and generate_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        login(request, new_user)
        return redirect ('/login')
    
    else:
        return render(request, 'activation_failed.html')
    

